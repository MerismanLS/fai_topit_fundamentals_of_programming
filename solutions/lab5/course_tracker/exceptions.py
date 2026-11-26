class CourseTrackerError(Exception):
    """Базовое исключение приложения CourseTracker."""


class ValidationError(CourseTrackerError):
    """Ошибка валидации данных модели или аргументов."""


class NotFoundError(CourseTrackerError):
    """Запрашиваемый объект (студент, работа, попытка) не найден."""


class DuplicateError(CourseTrackerError):
    """Попытка создать объект с уже существующим идентификатором."""


class StorageError(CourseTrackerError):
    """Ошибка чтения, записи или импорта/экспорта файлов."""
