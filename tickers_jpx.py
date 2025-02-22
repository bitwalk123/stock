from structs.res import AppRes

if __name__ == '__main__':
    # JPX ticker list
    res = AppRes()
    df = res.getJPXTickerList()
    print(df)
