class ExpirationTypeLookup:
    """
    Lookup for warranty expiration types
    """

    WARRANTY_EXPIRATION_STATUS_EXPIRED = 1    
    WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR = 2
    WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR_PLUS = 3
    WARRANTY_EXPIRATION_STATUS_EXPIRES_UNKNOWN = 4

    def __init__(self, id:int):
        self.id = id
        match self.id:
            case ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRED:
                self.description = "Warranty Expired"
            case ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR:
                self.description = "Warranty Expires in a year or less"
            case ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR_PLUS:
                self.description = "Warranty Expires in more than a year" 
            case ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_UNKNOWN:
                self.description = "Warranty Expiration Unknown"



    @staticmethod
    def get_all_expiration_types():
        """
        Gets a tuple where all the items are the possible instances of the class ExpirationTypeLookup
        """
        return tuple(ExpirationTypeLookup(i) for i in ExpirationTypeLookup.get_all_expiration_type_ids())
    
    @staticmethod
    def get_all_expiration_type_ids():
        """
        Gets a tuple where are the items are integers representing the different expiration types.
        """
        return (ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRED, 
                ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR,
                ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_YEAR_PLUS,
                ExpirationTypeLookup.WARRANTY_EXPIRATION_STATUS_EXPIRES_UNKNOWN)   


    @staticmethod
    def IsValidExpirationTypeID(expiration_type_id:int):
        return expiration_type_id is None or expiration_type_id == 0 or expiration_type_id in  ExpirationTypeLookup.get_all_expiration_type_ids()
