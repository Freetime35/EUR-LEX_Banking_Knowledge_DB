from ekb.models.relation import LegalRelation, RelationType


def test_legal_relation_creation() -> None:
    relation = LegalRelation(
        source_celex="32022R2554",
        relation=RelationType.AMENDS,
        target_celex="32013R0575",
    )

    assert relation.source_celex == "32022R2554"
    assert relation.target_celex == "32013R0575"
    assert relation.relation is RelationType.AMENDS
