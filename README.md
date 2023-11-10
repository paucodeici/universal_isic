# Organisation

Each classification system has multiple level.

So from each classification system, you can query the number of levels and for a given level you can get the elements of the level under.

It means for example with NAF, you have:
- from universal_isic import NAFV2
- NAFV2.number_of_levels => return 5
- NAFV2.all_elements => return a list of all the elements
- NAFV2.get_elements(level=1, previous_levels=list[list[int|str]])
- NAFV2(level_1="A", level_2="01").convert_to(ISICV4)

It means we need to have something to know what are the sub elements of a given level.


ISIC
====

This is a copy of the repository you can find in gitlab behind the isic package for python.

Plan here is to use the same structure but extends it to all the national classification system in order to get seamless mapping between different systems.

This is just a Python-friendly way to reference revision 4 of the International
Standard Industrial Classification (ISIC).  It's the result of pulling down
`this URL`_ and formatting it into a native Python object.  For more
information, or to see this data in other original source formats, visit the UN
`here`_.

.. _this URL: https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/ISIC_Rev_4_english_structure.Txt
.. _here: https://unstats.un.org/unsd/classifications/Econ/isic


How Do I Use It?
----------------

It's really not very advanced.  Just import it and reference it however you
like:

.. code-block:: python

    from isic import ISIC


    print(ISIC["02"])  # "Forestry and logging"
    print(ISIC["B"])  # "Mining and quarrying"

It's also handy if you want to use it in a Django model:

.. code-block:: python

    from django.db import models
    from isic import ISIC


    class MyModel(models.Model):
        industry = models.CharField(max_length=5, choices=ISIC.items())


Installation
------------

It's on PyPi, so just install it with pip.

.. code-block:: shell

    $ pip install isic
