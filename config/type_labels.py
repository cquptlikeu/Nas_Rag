"""受控类型词表(枚举)—— Q2「类型」查询与 FileRecord.type_label 的单一真源。

占位初版:与 PRD §6 配方一致;最终词表在 S1 语料配方锁定时定稿。
新增 / 调整须随语料一并定稿,不得在脚本里散落字符串字面量
(ARCHITECTURE §5:type_label ∈ 本词表,与 Query.structured.type 精确相等)。
"""

from __future__ import annotations

from enum import Enum


class FileType(str, Enum):
    """粗粒度文件类型(资格矩阵的行;ARCHITECTURE AD-5)。"""

    PHOTO = "photo"
    VIDEO = "video"
    SCAN = "scan"
    STUDY = "study"
    NOTE = "note"
    MEDIA = "media"


class TypeLabel(str, Enum):
    """细粒度受控词表(Q2 类型查询用)—— 占位初版,S1 定稿。"""

    # 证件 / 凭证(扫描)
    INVOICE = "invoice"
    RECEIPT = "receipt"
    BILL = "bill"
    CONTRACT = "contract"
    CERTIFICATE = "certificate"
    # 学习 / 资料
    PAPER = "paper"
    EBOOK = "ebook"
    ARTICLE = "article"
    # 笔记
    NOTE = "note"
    # 影像
    PHOTO = "photo"
    VIDEO = "video"
    # 媒体(纯噪声,恒真负例)
    MUSIC = "music"
    RECORDING = "recording"
