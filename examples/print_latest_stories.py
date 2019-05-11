from hackernewslib.clients import create_client


def main():
    client = create_client()

    for item in client.new():
        if item.type == "story":
            print("{title}\n{url}\n\n".format(title=item.title, url=item.url))


if __name__ == "__main__":
    main()
