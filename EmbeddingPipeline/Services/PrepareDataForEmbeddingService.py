from Helpers.Logger import get_logger

class PrepareDataForEmbeddingService:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)   
        
    def build_text(self, fetched_data):
        try:
            prepared_data = []
            for item in fetched_data:
                text = (
                    f"Tytuł ogłoszenia: {self.get_or_default(item["Title"])} "
                    f"Url ogłoszenia: {self.get_or_default(item['Url'])} "
                    f"Cena: {self.get_or_default(item['Price'])} "
                    f"Cena za metr kwadratowy: {self.get_or_default(item['PricePerM2'])} "
                    f"Powierzchnia: {self.get_or_default(item['Area'])} "
                    f"Ogrzewanie: {self.get_or_default(item['Heating'])} "
                    f"Czynsz: {self.get_or_default(item['Rent'])} "
                    f"Rynek: {self.get_or_default(item['Market'])} "
                    f"Adres: {self.get_or_default(item['Address'])} "
                    f"Opis: {self.get_or_default(item['Description'])} "
                    f"Liczba pokoi: {self.get_or_default(item['Rooms'])} "
                    f"Piętro: {self.get_or_default(item['Floor'])} "
                    f"Stan budynku: {self.get_or_default(item['BuildingCondition'])} "
                    f"Dostępne od: {self.get_or_default(item['AvailableFrom'])} "
                    f"Dodatkowe informacje: {self.get_or_default(item['AdditionalInfo'])} "
                    f"Rodzaj oferty: {self.get_or_default(item['OfferType'])} "
                    )
                prepared_data.append(text)
            return prepared_data
        except Exception as e:
            self.logger.error(f"Error while building text for embedding: {e}")
            return []
            
    def get_or_default(self, value):
        return str(value).strip() if value not in [None, "", "null", "None"] else "brak informacji"
