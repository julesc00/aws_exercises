

cookie_string = "cookies=value_sample"
cookie_index = cookie_string.find("=")

print(cookie_index)
print(cookie_string[cookie_index+1:])

origin = {
    "Records": [
        {
            "cf": {
                "config": {
                    "distributionDomainName": "d111111abcdef8.cloudfront.net",
                    "distributionId": "EDFDVBD6EXAMPLE",
                    "eventType": "origin-response",
                    "requestId": "4TyzHTaYWb1GX1qTfsHhEqV6HUDd_BzoBZnwfnvQc_1oF26ClkoUSEQ=="
                },
                "request": {
                    "clientIp": "203.0.113.178",
                    "headers": {
                        "x-forwarded-for": [
                            {
                                "key": "X-Forwarded-For",
                                "value": "203.0.113.178"
                            }
                        ],
                        "user-agent": [
                            {
                                "key": "User-Agent",
                                "value": "Amazon CloudFront"
                            }
                        ],
                        "via": [
                            {
                                "key": "Via",
                                "value": "2.0 8f22423015641505b8c857a37450d6c0.cloudfront.net (CloudFront)"
                            }
                        ],
                        "host": [
                            {
                                "key": "Host",
                                "value": "example.org"
                            }
                        ],
                        "cache-control": [
                            {
                                "key": "Cache-Control",
                                "value": "no-cache"
                            }
                        ]
                    },
                    "method": "GET",
                    "origin": {
                        "custom": {
                            "customHeaders": {},
                            "domainName": "example.org",
                            "keepaliveTimeout": 5,
                            "path": "",
                            "port": 443,
                            "protocol": "https",
                            "readTimeout": 30,
                            "sslProtocols": [
                                "TLSv1",
                                "TLSv1.1",
                                "TLSv1.2"
                            ]
                        }
                    },
                    "querystring": "",
                    "uri": "/"
                },
                "response": {
                    "headers": {
                        "access-control-allow-credentials": [
                            {
                                "key": "Access-Control-Allow-Credentials",
                                "value": "true"
                            }
                        ],
                        "access-control-allow-origin": [
                            {
                                "key": "Access-Control-Allow-Origin",
                                "value": "*"
                            }
                        ],
                        "date": [
                            {
                                "key": "Date",
                                "value": "Mon, 13 Jan 2020 20:12:38 GMT"
                            }
                        ],
                        "referrer-policy": [
                            {
                                "key": "Referrer-Policy",
                                "value": "no-referrer-when-downgrade"
                            }
                        ],
                        "server": [
                            {
                                "key": "Server",
                                "value": "ExampleCustomOriginServer"
                            }
                        ],
                        "x-content-type-options": [
                            {
                                "key": "X-Content-Type-Options",
                                "value": "nosniff"
                            }
                        ],
                        "x-frame-options": [
                            {
                                "key": "X-Frame-Options",
                                "value": "DENY"
                            }
                        ],
                        "x-xss-protection": [
                            {
                                "key": "X-XSS-Protection",
                                "value": "1; mode=block"
                            }
                        ],
                        "content-type": [
                            {
                                "key": "Content-Type",
                                "value": "text/html; charset=utf-8"
                            }
                        ],
                        "content-length": [
                            {
                                "key": "Content-Length",
                                "value": "9593"
                            }
                        ]
                    },
                    "status": "200",
                    "statusDescription": "OK"
                }
            }
        }
    ]
}

print(origin["Records"][0]["cf"]["response"]["headers"]["access-control-allow-origin"][0]["value"])