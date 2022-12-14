# -*- coding: utf-8 -*-
"""
@Time    : 2022/12/14 11:07
@Author  : itlubber
@Site    : itlubber.art
"""

import os
import re
import time
import traceback
from pyChatGPT import ChatGPT
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, ERROR


def get_logger(log_format="[ %(levelname)s ][ %(asctime)s ][ %(filename)s:%(funcName)s:%(lineno)d ] %(message)s", filename=None, stream=True):
    logger = getLogger("lubber")
    logger.setLevel(INFO)
    formatter = Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    if filename:
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except Exception as error:
                print(f'错误 >> 创建日志目录失败,清手动创建目录文件位置,运行 sudo mkdir -p {os.path.dirname(filename)}')
                print('错误 >> 报错信息 : {}'.format(error))

        fh = TimedRotatingFileHandler(filename=filename, when='D', backupCount=30, encoding="utf-8")
        fh.setLevel(INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        fh.close()

    if stream:
        ch = StreamHandler()
        ch.setLevel(INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        ch.close()

    return logger


def load_data(dir):
    files = [os.path.join(dir, f) for f in os.listdir(dir)]

    texts = {}
    for f in files:
        key = ".".join(os.path.basename(f).split(".")[:-1])
        texts[key] = []

        with open(f, "r", encoding="utf-8") as reader:
            for line in reader.readlines():
                if len(line.strip()) > 0:
                    texts[key].append(re.sub("[\r\n\t\s]{1,}", "", line.strip()))

    return texts


def dump_data(lines, file):
    with open(file, 'w+', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
            f.write("\n")


def get_response(query):
    try:
        response = chat.send_message(query)
        return response["message"]
    except ValueError:
        logger.error(traceback.format_exc())
        time.sleep(10.0)
        return ""


logger = get_logger(filename="logs/chatgpt.log")
session_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..XEkgE48zOTCWRvnB.ZkhlyuztMUG4tsrR8gwkDjuKyxNiMFS2wDBZWpRHdniJE8YsvGyGq1Sp9A6XBitdlzgZpVQZ0ktl7FODC5u2Ss2VKIubHZ9n_oIgwhpEWp-ZZ_Nes49AMi8iTURkHGf-z0h9XKIVXy2wzqJWVPnc-uyvZ0cLSBgLBnELdnDllJNqc6XqQh1yaFf6P0YNmXXZlLQ_NX-h9fr5tIAd_7J27Ya_7QaVozMdGWhSs4aYO42x7_R_KjsnldNHxHcGMullMsUge5gCO9ElP5R6UU6q_PT6H_CxijFjdhF1MQa8j7_WsB_gwrBxoCUUtECurWvmYsLY0V26hlLP9-Nllx4uvPX_2w61bD_Cm7jZpoB5phbCEE59CeCQ_u55KIoWNtwLNgrUJHGxnuUWQ7JvL6EzsIwMJkx3HLNBezTYqm7JOuAJPAdJM08HP6C4n_ore4hyQqQHErEErDfWEgsaGwhRjKY8Fb-qpFplLpo1uKd3EWIn4_hhXnGBV2sYMLe4NbwMhFiDSGDZkUtqpfRwWBTvndPuZmOQypv5qM3mfV4hekCOSRfTS4JFOuZFd_-gFHFDwpQBD-QknA9YNLsiMZGaXt0X2Gu0wuMGaYufTtQaiROUEBVad7tzJxr7pw7NRbDlzndxRJMpGq5tvBvQoywYD7KvK5RXOo8BjBcoi9asULKXTI6GrJM2JFAbB8oBtv8Dg-k3jcDL8khTQqGtkCxL6yRqmFzReIE0yS7qmiZ71mmrfVJ5P-W0WsaGX1gl70saBREtJT6WBkc8RSVL5mDIgtkfkmytK7cEb094mG4wIO1Schg6PUqoxwVpzfyBFeeGf33eCbxcMwbeI0mKbE9pLGthRXMXjyRjxpuZdnr3V_abCAe9VakAfu9Xl3qwquxmeJrWX4e3rz05PqV2TiaRY1EOJzIvgbsb5wJL9VIgI9Wb_7uYxt-8GSLywiAtq2mmnFr5oy5wmiqKDjTVW22eKNMCJomA81LD-sx7MljrlqCZQx9eSQr-VF9KUshEd9-SCU2g_CffLLS-KUC6fuSHX_Q4KtRhg9goOgK9-EhYanAiHUMrP_spsrxe0USBoZsmMXfErf3A-YxamtqFneJsTiyI0uJBgDy1LdlB1EZAUJu4DVrtF6l5T9IC3YaIe-wBbvCMve7HGQDgySlfH0vc1LOg6JSUl-qofGwVBmmVTv8yO5to2w_dHR-ZWeXB9QIwcxAPTuyjrM2Y2mUeP8hVu1F0_fObNcQNc1Fc-o5xT5pXu5j-yGXIIgTBDwRE-3igWLCYci7E39SeEH6xgORJ8I9uxHDCq5yrdPsbBxpzpgu6cW2T3LeGBzh_X8Huo9Zwl_B-IskvvN4VPPE7hjXEb_jCClbNEhS_UAsHZvfPGxmHtUVzqcUsxEY43n-_LcKEuFCBYVQdW8mRVYw403E59FJ1l8vCC2r9OK84ibOaT5JpnkreUiu9U00BdlrpD0X1EZTe4v5sK3lG98gX-Ye5iz5dMgayyfX6qcXQuSjMn4v41hl3g8LMw5Va0cx4BgHIYIPirw49iX3z1oG5VL9oI8feVlr_PRTtptrmSuMMYPS813xvtMAaNSrJIwRmyuOMQkiUuzfjun6QYjX5ctnQROT9g-YvC4ldm0DDJzgGv1KFxUtqIQCqVx-6A9E1pyHNQcspqqHfh1cdX9SKkp5FANkD_D-m81CpVwrt2JM0WmSBU7pNWtbh_zpkskpCJ5xc4WN6bPI1wehSYEYpl7CPrMbwsbo0ISMEURBaP-37XZWCG9E2a0U9OyfXXvaF0dbV1pY7CFjt8LrPtzVZ4QuUAZXOMHnx0L3z5qp0dTcCZfrGjjoIeyNC59awA11sR6i6hyvxJLwMCiyX4f4jFZ5hSJXB3TsQI_EXFYBliWk13hLjZAxJjFTzKtv6K_RPl_Ee6gItGaawAXUemsmPzL4WFzncbb0AfT77fzXndBl92CkUoQMl_GapLH7Wbf8gaTbivBBEaBnxmmFKtePYqxGhiSI4RmrRI7EXX4sswV2nFiz5mSEoku49JFq3Rng2L1KAZ1NF1_hXtxk5xTbV8RSLqNH2zPwlylcYV7pA08kmyR29XxN39C9NgEyaKCtkK2tv8NHf_Y5CiJCl4BF0Ik7MK1UMfNGhImZ5Zgzy8sG_dMKlJPEPcYbQezWT9UPjC-hqUzpr5WQS9Or9WDKCduI81VHESixPgobRecTYWN79hdrVy5HYsX3rSQyCgr-W7GbY_Ns9fFy_WqaqnlU4g8iosfPtU2SHf66DK86B8w0REM9U4CCIsbLFJu4Ckz26xRSQvsRyyB1kpOmn_q9S6MrpSgt3hKqdqs1e_mrMrxiwKoPRgHU55s8-ATnByMhIF3rLdX_7jAL7ARtESQ.UbE1_edLM-wPG_H1p8GALw"
chat = ChatGPT(session_token, proxy="http://127.0.0.1:7890", verbose=False)


texts = load_data("data/raw_data")

results = {}
for k, lines in texts.items():
    results[k] = []

    for line in lines:
        if len(results[k]) > 0:
            dump_data(results[k], f"data/gen_data/{k}_pairs.txt")

        chat.reset_conversation()

        query = f"根据下面提供的文本内容自动生成问答对：{line}"
        logger.info(query)

        time.sleep(10.0)
        response = get_response(query)
        logger.info(response)
        if response:
            results[k].append(response)

        if len(line) > 50:
            for i in range(3):
                time.sleep(10.0)
                response = get_response("继续根据文本内容生成更多的问答对")
                logger.info(response)
                if response:
                    results[k].append(response)
                else:
                    break


chat.close()
