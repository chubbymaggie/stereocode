##
# @file xslt_utils.py
#
# @copyright Copyright (C) 2013-2014 srcML, LLC. (www.srcML.org)
# 
# The stereocode is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# The stereocode Toolkit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with the stereocode Toolkit; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import stereocode, lxml, lxml.etree as et, re

xmlNamespaces = dict(src="http://www.sdml.info/srcML/src", cpp="http://www.sdml.info/srcML/cpp")
stereotypeExtractingRe = re.compile(r"@stereotype (?P<stereotypes>[^\*]*)")

def executeTransform(xmlDocument, xsltDocument):
    """
    This will need to do more in the future like setting up possible parameters
    and register other possible extension functionality associated with the
    XSLT document.
    """
    return xsltDocument(xmlDocument)

def executeAndTestTransform(unitTestInstance, xmlDocument, xsltDocument, expectedData):
    try:
        resultingDoc = executeTransform(xmlDocument, xsltDocument)
        
    except:
        print "Failed to execute transformation"
        raise

    matches = []
    try:
        matches = resultingDoc.xpath(
            "//src:function[preceding-sibling::*[1][self::src:comment]]",
            namespaces=xmlNamespaces
        )
        unitTestInstance.assertEqual(
            expectedData["matchesWithAStereotype"],
            len(matches),
            "Incorrect # of stereotypes. Expected: {0} Actual: {1}".format(expectedData["matchesWithAStereotype"], len(matches))
        )
        
        for testData in zip(matches, expectedData["functionInfo"]):
            unitTestInstance.assertIsNotNone(testData[0], "Invalid matched stereotype function.")
            stereotypeMatch = stereotypeExtractingRe.search(testData[0].getprevious().text)
            if stereotypeMatch == None:
                unitTestInstance.assertIsNone(
                    testData[1],
                    "This may indicate an invalid match. Stereotype has invalid comment before itself that is not recognized as a stereotype: {0} ".format(testData[0].getprevious().text)
                )
            else:
                methodStereotypes = [x.lower() for x in stereotypeMatch.group("stereotypes").strip().split(" ")]
                unitTestInstance.assertSetEqual(
                    set(testData[1][1]),
                    set(methodStereotypes),
                    "Mismatched between expected and actual stereotypes. Expected: {0}. Actual: {1}.".format(testData[1][1], methodStereotypes)
                )
    except:
        print "Failed to test stereotype data"
        print "transformed document"
        print et.tostring(resultingDoc)

        print "\n\n\nMatches: "
        for m in matches:
            print et.tostring(m)
        raise
    pass