import json
import logging

import aioboto3
from fastapi import Body, FastAPI, Query, Path
from starlette.requests import Request
from starlette.responses import Response
from telemetry_helper import OTLPInstrumentator

from src.auth import authentication_middleware
from src.enums import BedrockServices, Boto3BedrockMethods
from src.middleware import boto3_exception_handling_middleware
from src.settings import settings
from src.tagging import (
    is_resource_owner,
    TagResourceService,
    TagBedrockResourceStrategy,
    TagBedrockAgentsResourceStrategy,
    require_resource_ownership,
)
from src.utils import (
    json_serial,
    maybe_get_assume_role_creds,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

app = FastAPI()
app.middleware("http")(authentication_middleware)
app.middleware("http")(boto3_exception_handling_middleware)


if settings.env != "local":
    OTLPInstrumentator.init_telemetry(app, settings)


async def proxy_request(service_name, method, payload):
    assume_role_credentials = await maybe_get_assume_role_creds()
    session = aioboto3.Session()
    async with session.client(
        service_name, region_name=settings.aws_region, **assume_role_credentials
    ) as client:
        response = await getattr(client, method)(**payload)
        # This is needed to adjust content-length when parsing the response.
        response["ResponseMetadata"]["HTTPHeaders"].pop("content-length")
        return Response(
            content=json.dumps(response, default=json_serial),
            status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            headers=response["ResponseMetadata"]["HTTPHeaders"],
        )


@app.get("/")
@app.get("/_health")
async def health():
    return {"message": "OK"}


@app.post("/guardrails")
async def create_guardrail(request: Request, payload: dict = Body(...)):
    service = BedrockServices.BEDROCK
    response = await proxy_request(
        service, Boto3BedrockMethods.CREATE_GUARDRAIL, payload
    )
    owner_name = request.state.authorized_user.sub
    guardrail_arn = json.loads(response.body)["guardrailArn"]
    tagging_service = TagResourceService(
        service, settings.aws_region, TagBedrockResourceStrategy()
    )
    await tagging_service.tag_resource(guardrail_arn, {"Owner": owner_name})

    return response


@app.post("/guardrails/{guardrailIdentifier}")
@require_resource_ownership(BedrockServices.BEDROCK, "guardrail_identifier")
async def create_guardrail_version(
    request: Request,
    payload: dict = Body(...),
    guardrail_identifier: str = Path(alias="guardrailIdentifier"),
):
    payload["guardrailIdentifier"] = guardrail_identifier
    return await proxy_request(
        BedrockServices.BEDROCK, Boto3BedrockMethods.CREATE_GUARDRAIL_VERSION, payload
    )


@app.get("/guardrails/{guardrailIdentifier}")
@require_resource_ownership(BedrockServices.BEDROCK, "guardrail_identifier")
async def get_guardrail(
    request: Request,
    guardrail_identifier: str = Path(alias="guardrailIdentifier"),
    guardrail_version: str | None = Query(None, alias="guardrailVersion"),
):
    payload = {"guardrailIdentifier": guardrail_identifier}
    if guardrail_version:
        payload["guardrailVersion"] = guardrail_version

    return await proxy_request(
        BedrockServices.BEDROCK, Boto3BedrockMethods.GET_GUARDRAIL, payload
    )


@app.get("/guardrails")
async def list_guardrails(
    request: Request,
    guardrail_identifier: str | None = Query(None, alias="guardrailIdentifier"),
    max_results: int | None = Query(None, alias="maxResults"),
    next_token: str | None = Query(None, alias="nextToken"),
):
    payload = {
        key: value
        for key, value in {
            "guardrailIdentifier": guardrail_identifier,
            "maxResults": max_results,
            "nextToken": next_token,
        }.items()
        if value is not None
    }
    response = await proxy_request(
        BedrockServices.BEDROCK, Boto3BedrockMethods.LIST_GUARDRAILS, payload
    )
    owner_name = request.state.authorized_user.sub
    response_body = json.loads(response.body)
    guardrails = response_body["guardrails"]
    filtered_guardrails = [
        guardrail
        for guardrail in guardrails
        if await is_resource_owner(BedrockServices.BEDROCK, guardrail["arn"], owner_name)
    ]
    response_body["guardrails"] = filtered_guardrails
    return Response(
        content=json.dumps(response_body, default=json_serial),
        status_code=response_body["ResponseMetadata"]["HTTPStatusCode"],
        headers=response_body["ResponseMetadata"]["HTTPHeaders"],
    )


@app.put("/guardrails/{guardrailIdentifier}")
@require_resource_ownership(BedrockServices.BEDROCK, "guardrail_identifier")
async def update_guardrail(
    request: Request,
    payload: dict = Body(...),
    guardrail_identifier: str = Path(alias="guardrailIdentifier"),
):
    payload["guardrailIdentifier"] = guardrail_identifier
    return await proxy_request(
        BedrockServices.BEDROCK, Boto3BedrockMethods.UPDATE_GUARDRAIL, payload
    )


@app.delete("/guardrails/{guardrailIdentifier}")
@require_resource_ownership(BedrockServices.BEDROCK, "guardrail_identifier")
async def delete_guardrail(
    request: Request,
    guardrail_identifier: str = Path(alias="guardrailIdentifier"),
    guardrail_version: str | None = Query(default=None, alias="guardrailVersion"),
):
    payload = {"guardrailIdentifier": guardrail_identifier}
    if guardrail_version:
        payload["guardrailVersion"] = guardrail_version

    return await proxy_request(
        BedrockServices.BEDROCK, Boto3BedrockMethods.DELETE_GUARDRAIL, payload
    )


@app.post("/guardrail/{guardrailIdentifier}/version/{guardrailVersion}/apply")
@require_resource_ownership(BedrockServices.BEDROCK, "guardrail_identifier")
async def apply_guardrail(
    request: Request,
    payload: dict = Body(...),
    guardrail_identifier: str = Path(alias="guardrailIdentifier"),
    guardrail_version: str = Path(alias="guardrailVersion"),
):
    payload["guardrailIdentifier"] = guardrail_identifier
    payload["guardrailVersion"] = guardrail_version

    return await proxy_request(
        BedrockServices.BEDROCK_RUNTIME, "apply_guardrail", payload
    )


@app.post("/prompts/")
async def create_prompt(request: Request, payload: dict = Body(...)):
    service = BedrockServices.BEDROCK_AGENTS
    response = await proxy_request(service, Boto3BedrockMethods.CREATE_PROMPT, payload)
    owner_name = request.state.authorized_user.sub
    prompt_arn = json.loads(response.body)["arn"]
    tagging_service = TagResourceService(
        service, settings.aws_region, TagBedrockAgentsResourceStrategy()
    )
    await tagging_service.tag_resource(prompt_arn, {"Owner": owner_name})

    return response


@app.get("/prompts/{promptIdentifier}/")
@require_resource_ownership(BedrockServices.BEDROCK_AGENTS, "prompt_identifier")
async def get_prompt(
    request: Request,
    prompt_identifier: str = Path(alias="promptIdentifier"),
    prompt_version: str | None = Query(None, alias="promptVersion"),
):
    payload = {"promptIdentifier": prompt_identifier}
    if prompt_version:
        payload["promptVersion"] = prompt_version

    return await proxy_request(
        BedrockServices.BEDROCK_AGENTS, Boto3BedrockMethods.GET_PROMPT, payload
    )


@app.delete("/prompts/{promptIdentifier}/")
@require_resource_ownership(BedrockServices.BEDROCK_AGENTS, "prompt_identifier")
async def delete_prompt(
    request: Request,
    prompt_identifier: str = Path(alias="promptIdentifier"),
    prompt_version: str | None = Query(None, alias="promptVersion"),
):
    payload = {"promptIdentifier": prompt_identifier}
    if prompt_version:
        payload["promptVersion"] = prompt_version

    return await proxy_request(
        BedrockServices.BEDROCK_AGENTS, Boto3BedrockMethods.DELETE_PROMPT, payload
    )


@app.get("/prompts/")
async def list_prompts(
    request: Request,
    prompt_identifier: str | None = Query(None, alias="promptIdentifier"),
    max_results: int | None = Query(None, alias="maxResults"),
    next_token: str | None = Query(None, alias="nextToken"),
):
    payload = {
        key: value
        for key, value in {
            "promptIdentifier": prompt_identifier,
            "maxResults": max_results,
            "nextToken": next_token,
        }.items()
        if value is not None
    }
    response = await proxy_request(
        BedrockServices.BEDROCK_AGENTS, Boto3BedrockMethods.LIST_PROMPTS, payload
    )
    owner_name = request.state.authorized_user.sub
    response_body = json.loads(response.body)
    prompts = response_body["promptSummaries"]
    filtered_prompts = [
        prompt
        for prompt in prompts
        if await is_resource_owner(BedrockServices.BEDROCK_AGENTS, prompt["arn"], owner_name)
    ]
    response_body["prompts"] = filtered_prompts
    return Response(
        content=json.dumps(response_body, default=json_serial),
        status_code=response_body["ResponseMetadata"]["HTTPStatusCode"],
        headers=response_body["ResponseMetadata"]["HTTPHeaders"],
    )


@app.post("/prompts/{promptIdentifier}/")
@require_resource_ownership(BedrockServices.BEDROCK_AGENTS, "prompt_identifier")
async def create_prompt_version(
    request: Request,
    payload: dict = Body(...),
    prompt_identifier: str = Path(alias="promptIdentifier"),
):
    payload["promptIdentifier"] = prompt_identifier
    return await proxy_request(
        BedrockServices.BEDROCK_AGENTS, Boto3BedrockMethods.CREATE_PROMPT_VERSION, payload
    )


@app.put("/prompts/{promptIdentifier}/")
@require_resource_ownership(BedrockServices.BEDROCK_AGENTS, "prompt_identifier")
async def update_prompt(
    request: Request,
    payload: dict = Body(...),
    prompt_identifier: str = Path(alias="promptIdentifier"),
):
    payload["promptIdentifier"] = prompt_identifier
    return await proxy_request(
        BedrockServices.BEDROCK_AGENTS, Boto3BedrockMethods.UPDATE_PROMPT, payload
    )
