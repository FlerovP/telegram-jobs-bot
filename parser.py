import re
from typing import Dict, Optional

class JobParser:
    def __init__(self):
        # Регулярные выражения для извлечения информации
        self.patterns = {
            'salary': r'(?i)(?:зарплата|оплата|доход|зп):\s*([^\n]+)',
            'location': r'(?i)(?:локация|место|город):\s*([^\n]+)',
            'company': r'(?i)(?:компания|организация):\s*([^\n]+)',
            'contact': r'(?i)(?:контакт|связь|telegram|tg):\s*([^\n]+)',
            'requirements': r'(?i)(?:требования|навыки|скиллы|опыт):\s*([^\n]+)',
        }

    def extract_job_details(self, text: str) -> Dict[str, Optional[str]]:
        """
        Извлекает информацию о вакансии из текста сообщения.
        """
        # Базовая структура результата
        result = {
            'title': None,
            'company': None,
            'description': text,  # Полный текст как описание
            'salary': None,
            'location': None,
            'requirements': None,
            'contact': None
        }

        # Пытаемся определить заголовок (первая непустая строка)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('🔍', '💼', '📍', '💰', '📱', '✉️')):
                result['title'] = line
                break

        # Извлекаем остальную информацию с помощью регулярных выражений
        for key, pattern in self.patterns.items():
            match = re.search(pattern, text)
            if match:
                result[key] = match.group(1).strip()

        # Дополнительная обработка для улучшения результатов
        self._clean_results(result)
        
        return result

    def _clean_results(self, result: Dict[str, Optional[str]]):
        """
        Очищает и форматирует извлеченные данные.
        """
        for key, value in result.items():
            if value:
                # Удаляем лишние пробелы и специальные символы
                value = re.sub(r'\s+', ' ', value).strip()
                # Удаляем эмодзи и специальные символы
                value = re.sub(r'[^\w\s\-\.,;:@/]+', '', value).strip()
                result[key] = value

        # Если заголовок не был найден, пытаемся создать его из описания
        if not result['title'] and result['description']:
            first_line = result['description'].split('\n')[0].strip()
            if len(first_line) <= 100:  # Ограничиваем длину заголовка
                result['title'] = first_line
            else:
                result['title'] = first_line[:97] + "..." 