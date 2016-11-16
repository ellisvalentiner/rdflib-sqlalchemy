"""Convenience functions for working with Terms and Graphs."""
from rdflib import BNode
from rdflib import Graph
from rdflib import Literal
from rdflib import URIRef
from rdflib import Variable
from rdflib.graph import QuotedGraph
from rdflib.py3compat import format_doctest_out
from rdflib.term import Statement


SUBJECT = 0
PREDICATE = 1
OBJECT = 2
CONTEXT = 3
TERM_COMBINATIONS = dict([(term, index) for index, term, in enumerate([
     "UUUU", "UUUB", "UUUF", "UUVU", "UUVB", "UUVF", "UUBU", "UUBB", "UUBF",
     "UULU", "UULB", "UULF", "UUFU", "UUFB", "UUFF",
     #
     "UVUU", "UVUB", "UVUF", "UVVU", "UVVB", "UVVF", "UVBU", "UVBB", "UVBF",
     "UVLU", "UVLB", "UVLF", "UVFU", "UVFB", "UVFF",
     #
     "VUUU", "VUUB", "VUUF", "VUVU", "VUVB", "VUVF", "VUBU", "VUBB", "VUBF",
     "VULU", "VULB", "VULF", "VUFU", "VUFB", "VUFF",
     #
     "VVUU", "VVUB", "VVUF", "VVVU", "VVVB", "VVVF", "VVBU", "VVBB", "VVBF",
     "VVLU", "VVLB", "VVLF", "VVFU", "VVFB", "VVFF",
     #
     "BUUU", "BUUB", "BUUF", "BUVU", "BUVB", "BUVF", "BUBU", "BUBB", "BUBF",
     "BULU", "BULB", "BULF", "BUFU", "BUFB", "BUFF",
     #
     "BVUU", "BVUB", "BVUF", "BVVU", "BVVB", "BVVF", "BVBU", "BVBB", "BVBF",
     "BVLU", "BVLB", "BVLF", "BVFU", "BVFB", "BVFF",
     #
     "FUUU", "FUUB", "FUUF", "FUVU", "FUVB", "FUVF", "FUBU", "FUBB", "FUBF",
     "FULU", "FULB", "FULF", "FUFU", "FUFB", "FUFF",
     #
     "FVUU", "FVUB", "FVUF", "FVVU", "FVVB", "FVVF", "FVBU", "FVBB", "FVBF",
     "FVLU", "FVLB", "FVLF", "FVFU", "FVFB", "FVFF",
     #
     # "sUUU", "sUUB", "sUUF", "sUVU", "sUVB", "sUVF", "sUBU", "sUBB", "sUBF",
     # "sULU", "sULB", "sULF", "sUFU", "sUFB", "sUFF",
     #
     # "sVUU", "sVUB", "sVUF", "sVVU", "sVVB", "sVVF", "sVBU", "sVBB", "sVBF",
     # "sVLU", "sVLB", "sVLF", "sVFU", "sVFB", "sVFF"
])])

REVERSE_TERM_COMBINATIONS = dict(
    [(value, key) for key, value in TERM_COMBINATIONS.items()])

TERM_INSTANTIATION_DICT = {
    "U": URIRef,
    "B": BNode,
    "V": Variable,
    "L": Literal
}

GRAPH_TERM_DICT = {
    "F": (QuotedGraph, URIRef),
    "U": (Graph, URIRef),
    "B": (Graph, BNode)
}


@format_doctest_out
def normalize_graph(graph):
    """
    Take an instance of a ``Graph`` and return the instance's identifier and  ``type``.

    Types are ``U`` for a :class:`~rdflib.graph.Graph`, ``F`` for
    a :class:`~rdflib.graph.QuotedGraph` and ``B`` for a
    :class:`~rdflib.graph.ConjunctiveGraph`

    >>> from rdflib import plugin
    >>> from rdflib.graph import Graph, ConjunctiveGraph, QuotedGraph
    >>> from rdflib.store import Store
    >>> from rdflib import URIRef, Namespace
    >>> from rdflib_sqlalchemy.termutils import normalize_graph
    >>> memstore = plugin.get('IOMemory', Store)()
    >>> g = Graph(memstore, URIRef("http://purl.org/net/bel-epa/gjh"))
    >>> normalize_graph(g)
    (rdflib.term.URIRef(%(u)s'http://purl.org/net/bel-epa/gjh'), 'U')
    >>> g = ConjunctiveGraph(memstore, Namespace("http://rdflib.net/ns"))
    >>> normalize_graph(g)  #doctest: +ELLIPSIS
    (rdflib.term.URIRef(%(u)s'http://rdflib.net/ns'), 'U')
    >>> g = QuotedGraph(memstore, Namespace("http://rdflib.net/ns"))
    >>> normalize_graph(g)
    (rdflib.term.URIRef(%(u)s'http://rdflib.net/ns'), 'F')

    """
    if isinstance(graph, QuotedGraph):
        return graph.identifier, "F"
    else:
        return graph.identifier, term_to_letter(graph.identifier)


@format_doctest_out
def term_to_letter(term):
    """
    Relate a given term to one of several key types.

    * :class:`~rdflib.term.BNode`,
    * :class:`~rdflib.term.Literal`,
    * :class:`~rdflib.term.Statement` (Deprecated)
    * :class:`~rdflib.term.URIRef`,
    * :class:`~rdflib.term.Variable`
    * :class:`~rdflib.graph.Graph`
    * :class:`~rdflib.graph.QuotedGraph`

    >>> from rdflib import URIRef
    >>> from rdflib.term import BNode
    >>> # from rdflib.term import Statement
    >>> from rdflib.graph import Graph, QuotedGraph
    >>> from rdflib_sqlalchemy.termutils import term_to_letter
    >>> term_to_letter(URIRef('http://purl.org/net/bel-epa.com/'))
    'U'
    >>> term_to_letter(BNode())
    'B'
    >>> term_to_letter(Literal(%(u)s''))  # noqa
    'L'
    >>> term_to_letter(Variable(%(u)s'x'))  # noqa
    'V'
    >>> term_to_letter(Graph())
    'B'
    >>> term_to_letter(QuotedGraph("IOMemory", None))
    'F'
    >>> term_to_letter(None)
    'L'
    >>> # term_to_letter(Statement((None, None, None), None)) # Deprecated

    """
    if isinstance(term, URIRef):
        return "U"
    elif isinstance(term, BNode):
        return "B"
    elif isinstance(term, Literal):
        return "L"
    elif isinstance(term, QuotedGraph):
        return "F"
    elif isinstance(term, Variable):
        return "V"
    elif isinstance(term, Statement):
        return "s"
    elif isinstance(term, Graph):
        return term_to_letter(term.identifier)
    elif term is None:
        return "L"
    else:
        raise Exception(
            ("The given term (%s) is not an instance of any " +
             "of the known types (URIRef, BNode, Literal, QuotedGraph, " +
             "or Variable).  It is a %s")
            % (term, type(term)))


def construct_graph(key):
    """
    Return a tuple containing a ``Graph`` and an appropriate referent.

    Takes a key (one of 'F', 'U' or 'B')

    >>> from rdflib_sqlalchemy.termutils import construct_graph
    >>> construct_graph('F')
    (<class 'rdflib.graph.QuotedGraph'>, <class 'rdflib.term.URIRef'>)
    >>> construct_graph('U')
    (<class 'rdflib.graph.Graph'>, <class 'rdflib.term.URIRef'>)
    >>> construct_graph('B')
    (<class 'rdflib.graph.Graph'>, <class 'rdflib.term.BNode'>)

    """
    return GRAPH_TERM_DICT[key]


def triple_pattern_to_term_combinations(triple):
    """Map a triple pattern to term combinations (non-functioning)."""
    s, p, o = triple
    combinations = []
    if isinstance(o, Literal):
        for key, val in TERM_COMBINATIONS.items():
            if key[OBJECT] == 'O':
                combinations.append(val)
    return combinations


def type_to_term_combination(member, klass, context):
    """Map a type to a TermCombo."""
    try:
        rt = TERM_COMBINATIONS["%sU%s%s" %
                               (term_to_letter(member),
                                term_to_letter(klass),
                                normalize_graph(context)[-1])]
        return rt
    except:
        raise Exception("Unable to persist" +
                        "classification triple: %s %s %s %s" %
                        (member, "rdf:type", klass, context))


def statement_to_term_combination(subject, predicate, obj, context):
    """Map a statement to a Term Combo."""
    return TERM_COMBINATIONS["%s%s%s%s" %
                             (term_to_letter(subject), term_to_letter(predicate),
                              term_to_letter(obj), normalize_graph(context)[-1])]


def escape_quotes(qstr):
    """
    Escape backslashes.

    #FIXME:  This *may* prove to be a performance bottleneck and should
             perhaps be implemented in C (as it was in 4Suite RDF)

    Ported from Ft.Lib.DbUtil
    """
    if qstr is None:
        return ""
    tmp = qstr.replace("\\", "\\\\")
    tmp = tmp.replace("'", "\\'")
    return tmp
