class Filtrator:
    def filter_condition_parser(self, condition: str) -> Tuple[str, str, Union[str, float]]:
        result = re.split(r"(.+?)([><=]+)(.+)", condition)[1:-1]
        if not result:
            raise("неверный формат условия для фильтра")
        field, operator, value = result
        try:
            value = float(value)
        except ValueError:
            pass

        return field, operator, value
    
    def filter_data(self, data: List[Dict], condition: str) -> List[Dict]:
        field, operator, value = self.filter_condition_parser(condition)
        filtered_data = []
        if field not in data[0]:
            raise(f"поле '{field}' не найдено в данных")
        for item in data:
            if isinstance(value, float):
                if operator == ">" and float(item[field]) > value:
                    filtered_data.append(item)
                elif operator == "<" and float(item[field]) < value:
                    filtered_data.append(item)
                elif operator in ["=", "=="] and float(item[field]) == value:
                    filtered_data.append(item)
            elif operator in ["=", "=="] and item[field] == value:
                filtered_data.append(item)
        return filtered_data