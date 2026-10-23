"""Row-by-row authored routes. Left side is context; right side is optional or held."""
TABLE_ROUTES={
1: '''X01:A06 X01:A05 X01:A07 X01:R05 X01:R01 X01:A02 X01:A14 X01:A02 X01,H08:A14 X01:R03 X01,X22:A10 X01,X20:A11,F12 X01:A09 X01,X34:A10 X01,X28:G04 X01,X28:A08 X01,X29:R19 X01,X39,H08:B16 X01:A12''',
2: '''X02:B02 X02:B02 X02:A06 X02:A06 X02:A06 X02:A06 X02:A07 X02:A10 X02:A06 X03:D16 X02:A05 X03:D16 X03:A13 X03:A08 X03:R05 X03:A09 X03:A14 X03:G05 X03:A08''',
3: '''X03:A02 X03:A10 X03:R01 X03:R01 X03:F04 X03:A09 X03:R09 X03,H06:C09 X03:A03 X03,X22:A10 X03:F04 X03:R05 X03:A10 X03:A01 X03,X36:G04''',
4: '''X04:A01 X04:A06 X04:A05 X04:A02 X04:A02 X04:A02 X04:R02 X04:A03 X04:R01 X04:A04 X04,X42:R03 X04:A12 X04:A09 X04,X36:R04''',
5: '''X05:A06 X05:A08 X05:A07 X05:A07 X05:A07 X05:A05 X09:F04 X05:A07 X05:A07 X05:A12 X06:A02 X06: X06: X06: X13:D12 X05:A14 X05:A08 X28:A08 X06:A01 X06:A01''',
6: '''X07:A10 X07:A10 X07: X07:F04 X07:F04 X07:F04 X08: X08: X08: X08:''',
7: '''X09: X09: X09,H07: X09:R13 X09:F05 X09:F04 X09:F02 X09:F03 X09:F01 X09:F01 X09,H07: X09,H07:R13 X09,H07:R14''',
8: '''X10:D14 X10: X10: X10: X14: X10:F05 X11:F05 X11:F05 X11:F05 X12: X13:E13 X13:R09 X13: X15:C01 X15:C01 X13:R02 X21:''',
9: '''X10:D14 X11: X13:R09 X13:R09,R10 X09:R08 X09,H01: X09,H01: X09: X09,H02:F06 X42:F07 X16:R09 X16: X16: X17:G02 X17:R15 X17:D15 X17: X17:R07 X17,H04:R01 X18:B04 X18:A13''',
10: '''X19:B02 X19:A06 X19:A05 X19:D16 X01:A01 X21:R05 X21:A02 X21: X19:A10 X20:A11 X20:A11 X20:G01 X21:A11 X21:A09 X28:A08 X20:A10''',
11: '''X22:A10 X22: X22: X23: X23: X23: X25:R03 X25: X24: X23:A12''',
12: '''X26:G05 X26:A10 X26: X26:G05 X27:R19 X27: X28:A08 X28: X28: X29:R05 X29:R19 X28: X41:F09''',
13: '''X31: X31: X31: X30:C09 X30,H06:C09 X30:R06 X30,H06: X30,H06: X30:A10 X31: X31: X31: X31: X32,H06: X32: X30:R19''',
14: '''X33:G06 X33:R20 X33:B21 X33:B21 X33: X34: X34:''',
15: '''X35:G01 X35:G03 X35,H05: X35:G01 X35:G02 X35:G03 X35,H05: X35,H05: X35,H05:R18 X35,H05:R16 X35:R17 X35,H05: X35:R16 X29: X29: X36:G04 X36:G04 X36:R04 X36: X36:''',
16: '''X37:A11 X37:A11 X37:G05 X37:G05 X37: X37: X37:A11''',
17: '''X39:B01 X39:B02 X39:B03 X18:B04 X18:B05 X39:B06 X39:B07 X39:B08 X18:B09 X18:B10 X18:B11 X18:B12 X18:B13 X18:B04 X39:B15 X02:B14''',
18: '''X39:B17 X39:B16 X39:B16 X39:B18 X39:B19 X30:R12 X38:B20 X33:B21''',
19: '''X07:A10 X07:D02 X07:D03 X07:D01 X13:D04 X13:D05 X20:A10 X05:A07 X18:D17 X18:B04 X18:D18 X03,H04:D16 X05:A14 X10:D14 X17:D15 X20:E11 X20:A11 X23:A12''',
20: '''X15:C01 X15:C02 X15:C03 X15:C04 X15:C05 X15:C06 X13:C07 X15:C08 X30:C09 X15:C10 X15:C11 X30:C12 X30:C13 X21:C14''',
21: '''X38:E12 X13:E13 X38:E14 X38: X38:E15 X38: X38: X38:R22 X35:E01 X35:E02 X35:E03 X35:E04 X35:E05 X38:E06,E07 X38:E08,E09,E10 X41:''',
22: '''X03:D01 X13:D06 X13:D05 X13:D11 X13:D12 X13:D07 X13:D08 X13:D09 X13:R09 X13:R11 X09:R08 X09:D13,R08 X09:D10 X09,H03: X18:R21 X30:F09 X17,H04: X17,H04: X04:R01 X04:A02 X27:R19''',
23: '''X41:F08 X41:A10 X41:F09 X17:R15 X42:D12 X40:A14 X40:A02 X40: X41:D01 X41: X41:G01 X41:F10 X41:F11 X38:E15 X40: X41:F10'''
}

# Exact source comparison may supersede these only after implementation-time rebaselining.
def routes(reference,cards):
    by_id={c['id']:c for c in cards};result=[]
    for table in reference['tables'][:-1]:
        index=table['table_index'];spec=TABLE_ROUTES[index].split()
        assert len(spec)==len(table['rows'])-1,(index,len(spec),len(table['rows'])-1)
        for rowno,(row,route) in enumerate(zip(table['rows'][1:],spec),1):
            left,right=route.split(':');ctx=left.split(',');visual=right.split(',') if right else []
            assert all(x in by_id for x in ctx+visual),(index,rowno,ctx,visual)
            result.append(dict(id=f'K{len(result)+1:03d}',table_index=index,row_index=rowno,
                section=table['section'],term=row[0],seed_definition=row[1],
                context_card_ids=[x for x in ctx if x.startswith('X')],
                held_card_ids=[x for x in ctx if x.startswith('H')],optional_visual_card_ids=visual,
                activation='advisory_only',mapping_semantics='related_optional_realization_not_synonym_or_sufficient_definition',
                coverage_status='seed_retained_and_routed; not an independently validated clinical definition',
                source_ids=sorted({s for x in ctx+visual for s in by_id[x]['source_ids']})))
    return result
