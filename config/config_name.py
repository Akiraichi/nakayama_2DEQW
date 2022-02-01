from dataclasses import InitVar, dataclass, field


@dataclass(frozen=True)
class DefaultNameSetting:
    exp1_name: InitVar[str]
    exp1_index: InitVar[int]
    exp2_name: InitVar[str]
    default_folder_name: str = field(init=False)
    default_file_name: str = field(init=False)
    # default_top_folder_name: str = field(init=False, default="result2")
    # default_top_folder_name: str = field(init=False, default="result")
    default_top_folder_name: str = field(init=False, default="result_long_time")

    def __post_init__(self, exp1_name: str, exp1_index: int, exp2_name: str):
        object.__setattr__(self, "default_folder_name", f'{exp1_name}_{exp1_index}_{exp2_name}')
        object.__setattr__(self, "default_file_name", f'{exp1_name}_{exp1_index}_{exp2_name}')
