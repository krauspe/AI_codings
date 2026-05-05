def sortFqdns(fqdn_list):
    """groub by domain and sort by numerical part of hostname"""
    def sort_key(fqdn):
        domain = fqdn.split('.', 1)[1]
        hostname = fqdn.split('.', 1)[0]
        # Extract prefix and numeric part from hostname
        match = re.match(r'(\D+)(\d+)(-s\d+.*)', hostname)
        if match:
            prefix, num, rest = match.groups()
            return (domain, prefix, int(num), rest)
        return (domain, hostname)
    return sorted(fqdn_list, key=sort_key)


fqdn_list = [
  "psp1-s1.ak2.de",
  "psp1-s1.ak3.de",
  "psp1-s1.ak4.de",
  "psp1-s1.ak5.de",
  "psp10-s1.te1.de",
  "psp1-s1.te1.de",
  "psp2-s1.ak2.de",
  "psp2-s1.ak3.de",
  "psp2-s1.ak4.de",
  "psp2-s1.ak5.de",
  "psp2-s1.te1.de",
  "psp20-s1.te1.de",
  "psp1-s1.te1.de",
  "psp3-s1.ak2.de",
  "psp3-s1.ak3.de",
  "psp3-s1.ak4.de",
  "psp3-s1.ak5.de",
  "psp3-s1.te4.de",
  "psp4-s1.ak2.de",
  "psp4-s1.ak3.de",
  "psp4-s1.ak4.de",
  "psp4-s1.ak5.de",
  "psp4-s1.te2.de",
  "psp5-s1.ak2.de",
  "psp5-s1.ak3.de",
  "psp5-s1.ak4.de",
  "psp5-s1.ak5.de",
  "psp5-s1.te2.de",
  "psp6-s1.ak2.de",
]

sorted_fqdns = sortFqdns(fqdn_list)
for fqdn in sorted_fqdns:
    print(fqdn)

data = {
  psp1-s1.ak2.de: {
    mac: 001122334455,
    status: 'ok'
  }
  psp2-s1.ak3.de: {
    mac: 001122334455,
    status: 'ok'
  }
  psp2-s1.ak1.de: {
    mac: 001122334455,
    status: 'ok'
  }
  # ...
} 
  

for fqdn, parms in data.items(): # howto sort data.items() ?
    print(fqdn)
    do_something_with(data)

