import re


class AbstractHTMLParser:
    """
    This is an abstract class for a html parser.
    """
    def parse_html(self, soup):
        """
        This method takes a beautiful soup soup as input, and returns a list
        of parsed paragraphs.
        :param soup:
        :return: a list of paragraphs.
        """
        raise NotImplementedError("Should be implemented by concrete")


class SimpleHTMLParser(AbstractHTMLParser):
    """
    This is just a simple html parser, which pretty much just takes all the text in any
    paragraphs and returns it as a long string.
    """
    VALID_TAGS = ['div', 'p']

    def parse_html(self, soup):
        """
        This method just makes a naive run through the html, extracting all text in paragraphs.
        It returns a list of all paragraphs
        :param soup: The input html
        :return: A long string of all the text in paragraphs tags.
        """
        result = []
        for tag in soup.find_all('p'):
            s = tag.get_text()
            s = s.replace('\n', '')
            s = re.sub(" +", " ", s)
            if re.search("[0-9A-Fa-f]+", s) is not None:
                if not s.endswith("."):
                    s = s + "."
                result.append(s)
        return soup.title.text, result
