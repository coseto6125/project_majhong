# @Author: E-NoR
# @Date:   2023-04-21 22:25:21
# @Last Modified by:   E-NoR
# @Last Modified time: 2023-04-24 00:27:34

def check_chow(hand:list, idx:int)->int:
    """> 該函數檢查麻將手牌中給定的一組三張牌是否構成set，如果是，則返回最小的牌值。.

    Args:
      hand (list): 手牌
      idx (int): 我們要檢查 chow 的手中牌的索引。


    Returns:
      一個整數，代表給定手牌中指定索引 (idx) 和兩個相鄰索引處的三個牌中的最小值，從所有三個牌中減去相同的值後。
      如果套牌沒有形成有效的組合，則該函數返回 0。
    """
    suit_idx = idx // 9
    if suit_idx != (idx + 1) // 9 or suit_idx != (idx + 2) // 9:
        return 0
    if (smallest := min(hand[idx], hand[idx + 1], hand[idx + 2])) > 0:
        hand[idx : idx + 3] = [x - smallest for x in hand[idx : idx + 3]]
    return smallest


def check_4_sets(hand:list)->bool:
    """> 該函數檢查給定的一手牌是否有四組（三組或一組連續的三個數字）。.

    Args:
      hand (list): 手牌的列表。


    Returns:
      函数 `check_4_sets` 返回一个布尔值，指示给定的一手牌是否可以形成四组（三组或一组连续的三个数字）。
    """
    found = 0
    for i in range(len(hand)):
        if hand[i] > 2:
            hand[i] -= 3
            found += 1
        if i + 2 < len(hand):
            found += check_chow(hand, i)
    return found == 4


def check_hu(hand:list[int]):
    """> 該函數檢查給定的一手牌是否滿足特定類型麻將游戲中獲勝手的條件。.

    Args:
      hand (list[int]): 列表中的每個元素代表不同類型的牌，元素的值代表手中該類型牌的數量。
    Returns:
      一個布爾值（true或false），取決於輸入的手是否滿足特定類型麻將游戲中獲勝手的條件。
    """
    if check_13_19(hand):
        return True
    if check_7_dui(hand):
        return True
    if any(hand[i]==1 for i in range(27,34)):
        return False
    for i in range(len(hand)):
        remaining_hand = list(hand)
        remaining_hand[i] -= 2
        if check_4_sets(remaining_hand):
            return True
    return False

def check_gates(hand_card:list[int]) -> list[int]:
    """> 該函數檢查給定的一手牌是否可以形成獲勝手牌。。.

    Args:
      hand_card (list[int]):
        代表玩家手中麻將牌的 13 個整數列表。每個整數代表特定類型的圖塊數量（總共有 34 種類型）。
    Returns:
      則返回一個列表，其中包含當前所有聽的牌。
    """
    if sum(hand_card) != 13:
        raise ValueError("產出聽牌列表需要提供13張手牌")
    is_winning_tile = [False for _ in range(34)]
    for i in range(34):
        if hand_card[i] == 4:
            continue
        new_hand = list(hand_card)
        new_hand[i] += 1
        if check_hu(new_hand):
            is_winning_tile[i] = True
    winning_tiles_indices = [i + 1 for i, j in enumerate(is_winning_tile) if j]
    print_hand_winning(hand_card, winning_tiles_indices)
    return winning_tiles_indices

def print_hand_winning(hand:list[int], winning) -> None:
    """> 此函數採用表示麻將牌和獲勝牌的列表，並以可讀格式打印手牌和獲勝牌。.

    Args:
      hand (list[int]): 一個包含 34 個整數的列表，表示麻將牌中每種類型的牌數。
      winning: 參數“winning”是一個整數列表，表示遊戲中聽的牌。
    """
    actual_hand = []
    for i in range(34):
        actual_hand.extend([i + 1] * hand[i])
    print(f"Hand: {actual_hand} Winning tiles: {str(winning)}")

def check_7_dui(cards)->bool:
    """> 檢查是否符合七對子.

    Args:
      cards: 手牌列表。


    Returns:
      當所有手牌都為 兩張，且共14張，則返回七對子。
    """
    return all(v not in {1,3,4} for v in cards) and sum(cards) == 14

def check_13_19(cards)->bool:
    """> 函数检查麻将牌的给定手牌是否可以使用 13 orphans (十三什么) 的胡牌规则。.

    Args:
      cards: 表示一组麻將手牌。.

    Returns:
      一个布爾值，True 或 False。
    """
    total = 0
    index_tbl = [1, 9, 10, 18, 19, 27, 28, 29, 30, 31, 32, 33, 34]
    for i in index_tbl:
        c = cards[i - 1]
        if c not in {1, 2}:
            return False
        total += c
    return total == 14


if __name__ == "__main__":

    print("Mahjong calculator")
    cards = ([
            0, 2, 1, 1, 1, 1, 1, 1, 3,  # 1-9万 0-8
            0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1-9条 9-17
            0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1-9筒 18-26
            2, 0, 0, 0, 0, 0, 0  # 东南西北中发白 27-33
        ])
    print("驗證四面一雀，雀含字")
    assert check_gates(cards) == [2, 28],"驗證四面一雀，雀含字"


    cards = ([
            3, 3, 2, 0, 0, 2, 0, 0, 0,  # 1-9万
            0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1-9条
            0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1-9筒
            0, 3, 0, 0, 0, 0, 0  # 东南西北中发白
        ])
    print("驗證四面一雀，字非雀")
    assert check_gates(cards) == [3, 6], "驗證四面一雀，字非雀"

    cards = [
            1, 0, 0, 0, 0, 0, 0, 0, 1,  # 1-9万
            1, 0, 0, 0, 0, 0, 0, 0, 1,  # 1-9条
            1, 0, 0, 0, 0, 0, 0, 0, 1,  # 1-9筒
            1, 1, 1, 1, 1, 2, 0  # 东南西北中发白
        ]
    print("驗證國士無雙13么單張")
    assert check_gates(cards) == [34],"驗證國士無雙(十三么)單張"
    cards = [
            1, 0, 0, 0, 0, 0, 0, 0, 1,  # 1-9万
            1, 0, 0, 0, 0, 0, 0, 0, 1,  # 1-9条
            1, 0, 0, 0, 0, 0, 0, 0, 1,  # 1-9筒
            1, 1, 1, 1, 1, 1, 1  # 东南西北中发白
        ]
    print("驗證國士無雙13么13張")
    assert check_gates(cards) == [1, 9, 10, 18, 19, 27, 28, 29, 30, 31, 32, 33, 34],"驗證國士無雙(十三幺)13張"
    cards = [
            0, 0, 0, 0, 0, 0, 0, 0, 2,  # 1-9万
            0, 0, 0, 0, 0, 0, 0, 0, 2,  # 1-9条
            0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1-9筒
            2, 2, 2, 2, 0, 1, 0  # 东南西北中发白
        ]
    print("驗證七對子")
    assert check_gates(cards)==[33],"驗證七對子"
