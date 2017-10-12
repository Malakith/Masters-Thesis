import re
import bs4 as bs
from intervaltree import Interval, IntervalTree


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


class StyledHTMLParser(AbstractHTMLParser):
    """
    This parser tries to keep some of the typing, by keeping a list of bold and italic text, headers
    and whatnot.
    """

    STYLE_TAGS = ['b', 'strong', 'i', 'em', 'mark', 'small',
                  'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    INVIS_TAG = ['style', 'script', 'head', 'title', 'meta']

    def parse_html(self, soup):
        text, style = self.get_text_and_style(soup)
        tree = IntervalTree(Interval(begin, end, data) for begin, end, data in style)
        return text.strip(), tree

    def get_text_and_style(self, tag):
        if isinstance(tag, bs.Comment) \
                or isinstance(tag, bs.Declaration) \
                or isinstance(tag, bs.ProcessingInstruction) \
                or isinstance(tag, bs.Doctype) \
                or isinstance(tag, bs.CData) \
                or tag.name in self.INVIS_TAG:
            return "", []
        elif isinstance(tag, bs.element.NavigableString):
            result = re.sub(r'<!--.*?-->', "", tag.string.strip(), flags=re.S)
            return result, []
        else:
            ts = [self.get_text_and_style(c) for c in tag.children]
            offset = 0
            style = []
            for i in range(len(ts)):
                style += [[q[0] + offset, q[1] + offset, q[2]] for q in ts[i][1]]
                offset += len(ts[i][0]) + 1
            text = " ".join([k[0] for k in ts])
            if tag.name in self.STYLE_TAGS:
                style.append([0, len(text), tag.name])
        return text, style
