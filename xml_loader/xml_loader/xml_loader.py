from core.services.ucitati import UcitatiService
import xml.etree.ElementTree as ElemTree


class XmlLoader(UcitatiService):
    def name(self):
        return "XML Loader"

    def identifier(self):
        return "xml_loader"

    def ucitati(self):
        return "test"
