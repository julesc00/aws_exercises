#
# example_dict = {
#     "car": "a",
#     "animal": "dog"
# }
#
# print(example_dict.get("plant") or {})
#
#
# file_name = "Photo.JPEG"
# key_split = file_name.lower().rsplit(".", 1)
# print(key_split)
# if key_split[1] == "jpeg":
#     print(key_split[1])


def try_this():
    status_code = "OK"
    something = ""
    if something:
        status_code = "there is"
        return status_code
    return status_code


if __name__ == "__main__":
    print(try_this())
