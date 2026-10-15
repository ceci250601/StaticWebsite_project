from textnode import TextNode, TextType

def main():
    print(TextNode("Hello, World!", TextType.PLAIN, url="https://example.com"))

if __name__ == "__main__":
    main()