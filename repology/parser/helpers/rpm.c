#include <Python.h>

#include <stdio.h>
#include <rpm/header.h>

static PyObject* rpmread(PyUnicodeObject *path) {
	FD_t rpmfile = Fopen(argv[1], "r.ufdio");
	if (Ferror(rpmfile)) {
		PyErr_SetString(PyExc_RuntimeError, "Cannot open RPM file");
		return NULL;
	}

	Header header;
	while ((header = headerRead(rpmfile, HEADER_MAGIC_YES)) != NULL) {
		const char *errmsg = "unknown error";
		char *str = headerFormat(header, "%{name}|%{version}|%{packager}|%{group}|%{summary}\n", &errmsg);

		if (str != NULL) {
			fputs(str, stdout);
			free(str);
		} else {
			fprintf(stderr, "FATAL: cannot parse file: %s\n", errmsg);
			PyErr_SetString(PyExc_RuntimeError, "Cannot parse RPM file");
			Fclose(rpmfile);
			return 1;
		}
		headerFree(header);
	}

	Fclose(rpmfile);

	return PyLong_FromLong(123);
}

static PyMethodDef module_methods[] = {
	{"read", (PyCFunction)rpmread, METH_O, ""},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_definition = {
	PyModuleDef_HEAD_INIT,
	"repology.parser.helpers.rpm",
	NULL,
	-1,
	module_methods,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit__rpm(void) {
	return PyModule_Create(&module_definition);
}
