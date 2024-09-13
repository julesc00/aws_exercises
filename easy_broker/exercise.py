import requests

URL = "https://api.easybroker.com/v1/contact_requests"

sample_response = """
{
  "pagination": {
    "limit": 20,
    "page": 1,
    "total": 1,
    "next_page": null
  },
  "content": [
    {
      "id": 123,
      "name": "John Smith",
      "phone": "5559090909",
      "email": "mail@example.com",
      "contact_id": 123,
      "property_id": "EB-XXXX01",
      "message": "I'm interested in this property. Please contact me.",
      "source": "mydomain.com",
      "happened_at": "2020-03-01T23:26:53.402Z"
    }
  ]
}
"""



def get_data(url: str) -> None:
    response = requests.get(url)
    breakpoint()
    return response.text


if __name__ == "__main__":
    print(get_data(URL))
