"""State ID type definition."""
from backend.schemas import PropertyEnum


class StateIdName(str, PropertyEnum):
    TAX_ID = 'Tax ID'
    NPI_ID = 'NPI ID'
    MPTC_ID = 'MPTC ID'

    def describe(self):
        if self == self.TAX_ID:
            return "Tax Identification Number." \
                "Used to identify officers in New York State."
        elif self == self.NPI_ID:
            return "National Police Index ID. Assigned to officers" \
                " by the National Police Index."
        elif self == self.MPTC_ID:
            return "An ID assigned to officers by the Massachusetts Peace" \
                " Officer Standards and Training Commission."
