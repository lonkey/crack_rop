# Crack ROP

![Crack ROP](images/gadgets.jpg)

## Description

Crack ROP is a tool to format RP++ output. It needs the output from `!nmod` ([narly](https://code.google.com/archive/p/narly/downloads)) as input.

### What does it do?

It can turn RP++ output from this:
```
0x861e5: aaa ; adc bl, bh ; dec  [ebx+0x5B5E5FC7] ; leave ; retn 0x0004 ; (1 found)
0x90d21: aaa ; add  [eax], eax ; add al, ch ; add eax,  [eax] ; add byte [eax], al ; retn 0x0014 ; (1 found)
0x9275e: aaa ; add  [eax], eax ; retn 0x0008 ; (1 found)
0x8eda1: aaa ; add byte [eax], al ; add al, ch ; add eax,  [eax] ; add byte [eax], al ; retn 0x001C ; (1 found)
0x8a400: aaa ; add eax,  [eax] ; add byte [ebx-0x0007C36B], cl ; dec  [ebp-0x0007AF7B] ; call  [eax-0x75] ; (1 found)
0xc983b: aaa ; cld ; call  [eax-0x18] ; (1 found)
0xeb386: aaa ; cli ; call  [edi-0x18] ; (1 found)
0x84cfe: aaa ; cli ; dec ecx ; retn 0x000C ; (1 found)
```

To this:
```
rop += p32(ntdll_ba + 0xc983b)  # aaa; cld; call [eax-0x18]; (ntdll.dll:0x7740983b)
rop += p32(ntdll_ba + 0xeb386)  # aaa; cli; call [edi-0x18]; (ntdll.dll:0x7742b386)
rop += p32(ntdll_ba + 0x9275e)  # aaa; add [eax], eax; retn 0x0008; (ntdll.dll:0x773d275e)
rop += p32(ntdll_ba + 0x84cfe)  # aaa; cli; dec ecx; retn 0x000C;**** badchars: fe **** (ntdll.dll:0x773c4cfe)
rop += p32(ntdll_ba + 0x861e5)  # aaa; adc bl, bh; dec [ebx+0x5B5E5FC7]; leave; retn 0x0004; (ntdll.dll:0x773c61e5)
rop += p32(ntdll_ba + 0x90d21)  # aaa; add [eax], eax; add al, ch; add eax, [eax]; add byte [eax], al; retn 0x0014; (ntdll.dll:0x773d0d21)
rop += p32(ntdll_ba + 0x8eda1)  # aaa; add byte [eax], al; add al, ch; add eax, [eax]; add byte [eax], al; retn 0x001C; (ntdll.dll:0x773ceda1)
rop += p32(ntdll_ba + 0x8a400)  # aaa; add eax, [eax]; add byte [ebx-0x0007C36B], cl; dec [ebp-0x0007AF7B]; call [eax-0x75]; (ntdll.dll:0x773ca400)
```

Things to note:

* The gadgets are sorted by line length
* Formatted to copy/paste into a python script
* Bad characters are clearly marked
* The absolute address (based on the base address) is noted

### But I don't like `<insert something you don't like here>`!
No worries. Crack ROP uses a plugin system. All you need to do is modify (or create) a plugin to fix what you don't like.

## Getting Started

### Current(ish) version of RP++

You need to have a current version of RP++. Not all versions support the `--use-offsets` (`-o`) option. To get the 32bit versions of RP++ you can either compile it yourself or grab this copy from [vpzed](https://github.com/vpzed/osed/tree/main).

vpzed also created instructions for compiling it locally if you would prefer:
[https://github.com/vpzed/osed/blob/main/compile-rp-plus-win32.txt](https://github.com/vpzed/osed/blob/main/compile-rp-plus-win32.txt)

### Config file

The repo comes with a `config.ini.sample` file pre-populated with some sane defaults. Copy this to `config.ini` and modify it as desired. The `config.ini` file is not tracked by `git`.

### Save Narly Output

The script expects a path to Narly output. Within WinDBG simply do:

* `.load narly ; !nmod`

Copy the output to a text file. This is what you want to provide as the `input_file` for the script. Please note that the output from the script will be written to the same directory as the `input_file`.

### Running the script

Running `python crack_rop.py --help` will show you all available options:

```
usage: crack_rop.py [-h] [-g GADGET_SIZE] [-n] [-a] [-d] [-s] [-x] [-b BADCHARS] [-o] input_file

Parse nmod output and run rp++ on each.

positional arguments:
  input_file            Path to nmod output file.

options:
  -h, --help            show this help message and exit
  -g GADGET_SIZE, --gadget_size GADGET_SIZE
                        Maximum gadget size, default is 5
  -n, --allow_null      Allow the address to start with '00', default is False
  -a, --allow_aslr      Allow binaries protected by ASLR, default is False
  -d, --allow_dep       Allow binaries protected by DEP, default is False
  -s, --require_safe_seh_off
                        Only include binaries where SafeSEH is OFF, default is False
  -x, --auto-delete     Will not ask before deleting existing folders, default is False.
  -b BADCHARS, --badchars BADCHARS
                        Bad Characters (format: '\x00\x0a')
  -o, --use-offsets     Will use offsets instead of exact addresses.

Example: python crack_rop.py modules.txt
```

An example of running the script may look like:
```
python crack_rop.py -nadx "C:\Tools\test\modules.txt" -b "\xfe" -o
```

## Plugins

There are currently two types of plugins Lines, Post. Each plugin is expected to have a `main` function that gets called automatically.

### Line

Fires on each line read.

Each enabled line plugin receives the line and is expected to do whatever modifications required and then return the line.

The plugins work one after another and it is important that the order of the plugins in `config.ini` is maintained. Otherwise you could have an earlier plugin change the line in such a way that a later plugin cannot modify it as expected.

### Post

Fires after a file has been processes.

There is currently only one post plugin and that does a sort.
