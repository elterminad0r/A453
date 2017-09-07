# A453
From my GCSE computing course - see [my full writeup] here. It's a **heavily** type-annotated collection of scripts in Python, which perform various forms of naive and less naive compression on text. It initially uses a very naive system of building an index of words and writing "pointers" to words in that index, where the pointers are space-separated base-10 integers in ASCII. This is of course a tremendous waste of a byte - I later go on to use variable-length prefix encodings and raw binary data-files to make some significant gains. It's nowhere near something like LZW compression in terms of speed or compressive factor, but I think that for a Python script given the initial constraints, it's not bad at all. Also features some heavy unit testing, and modularisation, and a pretty decent interface for input/output using argparse.

The most simple compressive algorithm (`readable_compression.py`), given the input:

    ASK NOT WHAT YOUR COUNTRY CAN DO FOR YOU BUT WHAT YOU CAN DO FOR YOUR COUNTRY

produces the *readable* output:

    ASK NOT WHAT YOUR COUNTRY CAN DO FOR YOU BUT
    0 1 2 3 4 5 6 7 8 9 2 8 5 6 7 3 4

Which it can then correctly decode.


The more advanced `lossless_compression.py` can correctly encode something like this:

  Chor. Two households, both alike in dignity,
    In fair Verona, where we lay our scene,
    From ancient grudge break to new mutiny,
    Where civil blood makes civil hands unclean.
    From forth the fatal loins of these two foes
    A pair of star-cross'd lovers take their life;
    Whose misadventur'd piteous overthrows
    Doth with their death bury their parents' strife.
    The fearful passage of their death-mark'd love,
    And the continuance of their parents' rage,
    Which, but their children's end, naught could remove,
    Is now the two hours' traffic of our stage;
    The which if you with patient ears attend,
    What here shall miss, our toil shall strive to mend.
                                                         [Exit.]

in binary format, and decode it (by this command).

    $ python lossless_compression.py --input ../text/rom_ju_intro.txt  | python lossless_decompression.py

Yes, I have tested my lossless algorithm on the works of Shakespeare. It produces a lossless compressive ratio of about 40%.
