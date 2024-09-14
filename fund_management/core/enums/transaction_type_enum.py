from enum import Enum


class TransactionTypeEnum(Enum):
    SUBSCRIBE = 'subscribe'
    UNSUSCRIBE = 'unsuscribe'