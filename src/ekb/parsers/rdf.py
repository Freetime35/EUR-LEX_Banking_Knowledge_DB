from rdflib import Graph


class RdfParser:
    """Parse RDF serializations into an rdflib graph."""

    def parse(self, rdf_xml: str) -> Graph:
        """Parse RDF/XML content and return the resulting graph."""
        if not rdf_xml.strip():
            raise ValueError("RDF/XML content must not be empty.")

        graph = Graph()
        graph.parse(data=rdf_xml, format="xml")
        return graph