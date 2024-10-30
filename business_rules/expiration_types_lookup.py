class ExpirationTypeLookup:
    """
    Lookup for warranty expiration types
    """

    WARRANTY_EXPIRATION_STATUS_EXPIRED = 1    
    WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR = 2
    WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR_PLUS = 3
    WARRANTY_EXPIRATION_STATUS_EXPIRES_UNKNOWN = 4

    def __init__(self, id:int, description:str):
        self.id = id
        self.description = description

    @staticmethod
    def get_all_expiration_types():
        """
        Gets the expiration types
        """
        return (
            ExpirationTypeLookup(ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRED,"Warranty Expired" ), 
            ExpirationTypeLookup(ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR,"Warranty Expires in a year or less" ), 
            ExpirationTypeLookup(ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR_PLUS,"Warranty Expires in more than a year" ), 
            ExpirationTypeLookup(ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_UNKNOWN,"Warranty Expiration Unknown")
            )
