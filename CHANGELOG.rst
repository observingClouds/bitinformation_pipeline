=========
CHANGELOG
=========

X.X.X (unreleased)
------------------

* Drop python 3.8 support and add python 3.11 (:pr:`175`) `Hauke Schulz`_.
* Implement basic retrieval of bitinformation in python as alternative to julia implementation (:pr:`156`, :issue:`155`, :pr:`126`, :issue:`125`) `Hauke Schulz`_ with helpful comments from `Milan Klöwer`_.
* Make julia binding to BitInformation.jl optional (:pr:`153`, :issue:`151`) `Aaron Spring`_.

0.0.3 (2022-07-11)
------------------

* Fix julia package installations for PyPi and enable installation via pip and conda (:issue:`18`, :pr:`132`, :pr:`131`) `Filipe Fernandes`_, `Mark Kittisopikul`_.
* Fix compression example for zarr-files (:issue:`119`, :pr:`121`) `Hauke Schulz`_.
* Keep ``attrs`` as ``source_attribute`` from input in :py:func:`xbitinfo.xbitinfo.get_bitinformation`. (:issue:`154`, :pr:`158`) `Aaron Spring`_.

0.0.2 (2022-07-11)
------------------

* Fix ``kwargs`` in :py:func:`xbitinfo.xbitinfo._get_bitinformation_kwargs_handler` which were not reused for other variables in :py:func:`xbitinfo.xbitinfo.get_bitinformation`.
  (:issue:`99`, :pr:`101`) `Aaron Spring`_.
* Refactor :py:func:`xbitinfo.xbitinfo.get_keepbits` with xarray functions.
  (:pr:`100`) `Aaron Spring`_.
* Allow ``dim`` as ``list`` in :py:func:`xbitinfo.xbitinfo.get_bitinformation`.
  (:issue:`105`, :pr:`106`) `Aaron Spring`_.
* Fix PyPI package and make it actually installable via pip (:issue:`14`, :pr:`114`, :pr:`103`) `Aaron Spring`_, `Hauke Schulz`_, `Rich Signell`_.
* Improve PyPi packaging (:pr:`110`)  `Filipe Fernandes`_.

0.0.1 (2022-05-04)
------------------

* First release on PyPI.
