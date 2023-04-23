# @Author: E-NoR
# @Date:   2023-04-23 01:05:46
# @Last Modified by:   E-NoR
# @Last Modified time: 2023-04-24 00:40:02
from pprint import pprint

from pydantic import BaseModel, validator


class PublicData(BaseModel):
    game_no: int = 0  # 局號
    dealer_sit: int = 0  # 莊家座位
    remaining_tiles: int = 0  # 剩餘的牌數
    dora: list[int] = []  # 寶牌
    hai_dora: list[int] = []  # 開寶牌
    ura_dora: list[int] = []  # 裏寶牌
    round_wind: int = 0  # 圈風
    kang_count: int = 0  # 本場開槓的次數
    kang_sit: set[int] = set()  # 本場有槓牌的玩家

    def add_hai_dora(self, tile: int):
        # 增加開寶牌
        self.hai_dora.append(tile)
        self.dora.append(tile)

    def add_ura_dora(self, tile: int):
        # 增加裏寶牌
        self.ura_dora.append(tile)
        self.dora.append(tile)


class Meld(BaseModel):
    m_type: int = 0  # 0 順子，1 刻子，2 明槓，3 加槓，4 暗槓
    tiles: list[int] = []  # 面子牌所包含的牌的整數表示，列表中每個元素都是一張牌的整數表示


class Player(BaseModel):
    sit: int = 0  # 玩家座位
    name: str = ""  # 玩家名稱
    fu: int = 0  # 勝利玩家獲得的符數
    fan: int = 0  # 勝利玩家獲得的番數
    score: int = 25000  # 玩家分數
    points: int = 0  # 玩家獲得的點數
    tiles: list[int] = []  # 玩家手牌
    melds: list[Meld] = []  # 玩家的面子牌列表
    furiten: list[int] = []  # 玩家的振聽牌列表
    riichi: int = 0  # 0 未立值 1 立直 2 雙立直
    is_menqing: bool = False  # 是否為門清
    is_dealer: bool = False  # 是否為莊家
    is_wind: bool = False  # 是否為自風
    is_ippatsu: bool = False  # 是否一發
    is_tenpai: bool = False  # 是否聽牌
    is_rinshan: bool = False  # 是否嶺上開花
    is_chankan: bool = False  # 是否搶槓
    is_tsumo: bool = False  # 是否自摸
    is_haitei: bool = False  # 是否海底摸月
    is_houtei: bool = False  # 是否河底撈魚

    @validator("melds")
    def _set_is_menqing(cls, new_melds, values):
        # 是否為門清
        if values.get("is_menqing") and (not new_melds or new_melds[-1].m_type != 4):
            return False
        return values.get("is_menqing", True)


class Game(BaseModel):
    players: tuple[Player | None, ...]
    public: dict


sit_list = 1, 3, 5, 7
players = [Player(sit=sit) if sit not in sit_list else None for sit in range(max(sit_list))]
game = Game(players=tuple(players), public={})
pprint(game)
