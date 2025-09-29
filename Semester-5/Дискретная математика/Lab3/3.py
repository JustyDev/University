import sys
import bisect

input = sys.stdin.readline

# 1. Парсим RLE строку s в список block-ов [(char, len), ...]
def parse_rle(s):
    blocks = []
    n = len(s)
    i = 0
    while i < n:
        # если цифра, ищем всю группу (может быть несколько цифр, затем буква)
        if s[i].isdigit():
            num_start = i
            while i < n and s[i].isdigit():
                i += 1
            cnt = int(s[num_start:i])
            c = s[i]
            blocks.append( (c, cnt) )
            i += 1
        else:
            # просто буква, значит 1 шт
            c = s[i]
            blocks.append( (c, 1) )
            i += 1
    return blocks

def main():
    import sys
    import threading

    def run():
        s = sys.stdin.readline().strip()
        q = int(sys.stdin.readline())

        queries = []
        for _ in range(q):
            l, r = map(int, sys.stdin.readline().split())
            queries.append( (l, r) )

        blocks = parse_rle(s)
        # print(blocks)

        # [ (буква, count) ... ]
        prefix = [0]  # позиции конца блока-1 (0 индексация, 0 - пусто)
        for c, cnt in blocks:
            prefix.append(prefix[-1] + cnt)
        # Теперь prefix[i] - позиция конца блока i-1
        # 1-й блок: 1..prefix[1]
        # 2-й блок: prefix[1]+1 .. prefix[2]

        # Для каждого запроса l,r находим, какие блоки и на какие части попадают
        for l, r in queries:
            # Найти блок содержащий l, и блок содержащий r
            left = bisect.bisect_left(prefix, l)
            right = bisect.bisect_left(prefix, r)
            # левая граница внутри блока left, правая внутри блока right

            result = 0

            if left == right:
                # одна группа
                cnt_in_block = r - l + 1
                if blocks[left-1][1] == cnt_in_block:
                    # весь блок покрыт -- сожмётся в одну пару симв+число (или только буква)
                    result += len(str(cnt_in_block)) + 1 if cnt_in_block != 1 else 1
                else:
                    # только часть блока -- сожмётся как симв+число/симв
                    result += len(str(cnt_in_block)) + 1 if cnt_in_block != 1 else 1
            else:
                # левый крайний кусок
                lblock_total = prefix[left] - l + 1
                if lblock_total == blocks[left-1][1]:
                    result += len(str(lblock_total)) + 1 if lblock_total != 1 else 1
                else:
                    result += len(str(lblock_total)) + 1 if lblock_total != 1 else 1
                # правый крайний кусок
                rblock_total = r - prefix[right-1]
                if rblock_total == blocks[right-1][1]:
                    result += len(str(rblock_total)) + 1 if rblock_total != 1 else 1
                else:
                    result += len(str(rblock_total)) + 1 if rblock_total != 1 else 1
                # между ними целые блоки
                for i in range(left, right-1):
                    cnt = blocks[i][1]
                    result += len(str(cnt)) + 1 if cnt != 1 else 1
            print(result)

    threading.Thread(target=run,).start()

if __name__ == "__main__":
    main()
