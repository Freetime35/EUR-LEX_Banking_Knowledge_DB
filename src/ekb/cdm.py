from rdflib import URIRef


CDM_URI_PREFIX = "http://publications.europa.eu/ontology/cdm#"

RESOURCE_LEGAL_AMENDS = URIRef(
    f"{CDM_URI_PREFIX}resource_legal_amends_resource_legal"
)

RESOURCE_LEGAL_REPEALS = URIRef(
    f"{CDM_URI_PREFIX}resource_legal_repeals_resource_legal"
)

WORK_CITES = URIRef(
    f"{CDM_URI_PREFIX}work_cites_work"
)

RESOURCE_LEGAL_BASED_ON = URIRef(
    f"{CDM_URI_PREFIX}resource_legal_based_on_resource_legal"
)

RESOURCE_LEGAL_TYPE = URIRef(
    f"{CDM_URI_PREFIX}resource_legal_type"
)
