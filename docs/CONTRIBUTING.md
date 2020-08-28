# Contributing

Thank you very much for considering to contribute to our project. The devolo PLC devices deliver interesting data that we wanted to be usable in other projects. To achieve that goal, help is welcome.

The following guidelines will help you to understand how you can help. They will also make transparent to you the time we need to manage and develop this open source project. In return, we will reciprocate that respect in addressing your issues, assessing changes, and helping you finalize your pull requests.

## Table of contents

1. [Reporting an issue](#reporting-an-issue)
1. [Requesting a feature](#requesting-a-feature)
1. [Code style guide](#code-style-guide)

## Reporting an issue

If you are having issues with our module, especially, if you found a bug, we want to know. Please [create an issue](https://github.com/2Fake/devolo_plc_api/issues). However, you should keep in mind that it might take some time for us to respond to your issue. We will try to get in contact with you within two weeks. Please also respond within two weeks, if we have further inquiries.

## Requesting a feature

While we develop this module, we have our own use cases in mind. Those use cases do not necessarily meet your use cases. Nevertheless we want to hear about them, so you can either [create an issue](https://github.com/2Fake/devolo_plc_api/issues) or create a merge request. By choosing the first option, you tell us to take care about your use case. That will take time as we will prioritize it with our own needs. By choosing the second option, you can speed up this process. Please read our code style guide.

## Code style guide

We basically follow [PEP8](https://www.python.org/dev/peps/pep-0008/), but deviate in some points for - as we think - good reasons. If you have good reasons to stick strictly to PEP8 or even have good reasons to deviate from our deviation, feel free to convince us.

We limit out lines to 127 characters, as that is maximum length still allowing code reviews on GitHub without horizontal scrolling.

As PEP8 allows to use extra blank lines sparingly to separate groups of related functions, we use an extra line between static methods and constructor, constructor and properties, properties and public methods, and public methods and internal methods.

We use double string quotes, except when the string contains double string quotes itself or when used as key of a dictionary.

If you find code where we violated our own rules, feel free to [tell us](https://github.com/2Fake/devolo_plc_api/issues).

## Testing

We cover our code with unit tests written in pytest, but we do not push them to hard. We want public methods covered, but we skip nested and trivial methods. Often we also skip constructors. If you want to contribute, please make sure to keep the unit tests green and to deliver new ones, if you extend the functionality.
