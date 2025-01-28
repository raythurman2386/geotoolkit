from abc import ABC, abstractmethod


class BasePreprocessor(ABC):
    @abstractmethod
    def clean_field_names(self, dataset):
        pass

    @abstractmethod
    def standardize_projection(self, dataset, target_proj):
        pass


class BaseAnalyzer(ABC):
    @abstractmethod
    def calculate_statistics(self, dataset):
        pass

    @abstractmethod
    def perform_overlay(self, layer1, layer2, overlay_type):
        pass
