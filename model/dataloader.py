from torch.utils.data import Dataset
import pandas as pd


def make_df_windows(
    df, 
    T:t.Union[t.List, int]=140028, # no artigo, eles falaram que usam diferentes tamanhos de janelamento, então deixei aqui só pra caso a gente tente fazer o teste com mais tamanhos 
    H=128
):
    windows = []
    if isinstance(T, list):
        for k in T:
            window_len = k+H
            for i in range(1, df.shape[1]):
                for j in range(df.shape[0]-window_len-1):
                    windows.append(df.iloc[j:j+window_len, i].values)
    else:
        window_len = T+H
        for i in range(1, df.shape[1]):
            for j in range(df.shape[0]-window_len-1):
                windows.append(df.iloc[j:j+window_len, i].values)
    return windows


class DataLoader(Dataset):
    def __init__(
        self, 
        df, 
        T:t.Union[t.List, int]=140028, 
        H=128
    ):
        self.T = T 
        self.data = make_df_windows(df, T=T, H=H)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        return item[0:self.T], item[self.T:]