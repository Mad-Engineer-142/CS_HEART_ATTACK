import os
import pkgutil
import importlib
from pathlib import Path
import inspect


class BaseService:
    def search(self, query):
        raise NotImplementedError("Search method not implemented")


def create_adapter_class(service_class):
    class ServiceAdapter(BaseService):
        def __init__(self):
            self.service = service_class()

        def search(self, query):
            return self.service.search(query)

    return ServiceAdapter


def discover_services(package_name):
    services = {}
    package_path = Path(__file__).parent / package_name
    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        module = importlib.import_module(f"{package_name}.{module_name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if inspect.isclass(attribute) and issubclass(attribute, BaseService) and attribute != BaseService:
                services[module_name] = create_adapter_class(attribute)
    return services


services = discover_services('services')


class ServiceFactory:
    @staticmethod
    def get_service(service_name):
        Service = services.get(service_name)
        if Service:
            return Service()
        raise ValueError(f"Service '{service_name}' not found")


class ServiceManager:
    def __init__(self):
        self.items = []

    def addService(self, service_name, query):
        try:
            service = ServiceFactory.get_service(service_name)
            result = service.search(query)
            self.items.append({
                "source": service_name,
                "content": result
            })
        except ValueError as e:
            print(f"Error: {e}")

    def getServiceInfo(self):
        return self.items
