/* Copyright 2007-2010 Jozsef Kadlecsik (kadlec@blackhole.kfki.hu)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation.
 */
#include <libipset/data.h>			/* IPSET_OPT_* */
#include <libipset/parse.h>			/* parser functions */
#include <libipset/print.h>			/* printing functions */
#include <libipset/types.h>			/* prototypes */

/* Parse commandline arguments */
static const struct ipset_arg bitmap_port_create_args0[] = {
	{ .name = { "range", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_PORT,
	  .parse = ipset_parse_tcp_port,	.print = ipset_print_port,
	},
	{ .name = { "timeout", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_TIMEOUT,
	  .parse = ipset_parse_timeout,		.print = ipset_print_number,
	},
	/* Backward compatibility */
	{ .name = { "from", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_PORT,
	  .parse = ipset_parse_single_tcp_port,
	},
	{ .name = { "to", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_PORT_TO,
	  .parse = ipset_parse_single_tcp_port,
	},
	{ },
};

static const struct ipset_arg bitmap_port_add_args0[] = {
	{ .name = { "timeout", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_TIMEOUT,
	  .parse = ipset_parse_timeout,		.print = ipset_print_number,
	},
	{ },
};

static const char bitmap_port_usage0[] =
"create SETNAME bitmap:port range FROM-TO\n"
"               [timeout VALUE]\n"
"add    SETNAME PORT|FROM-TO [timeout VALUE]\n"
"del    SETNAME PORT|FROM-TO\n"
"test   SETNAME PORT\n\n"
"where PORT, FROM and TO are port numbers or port names from /etc/services.\n";

static struct ipset_type ipset_bitmap_port0 = {
	.name = "bitmap:port",
	.alias = { "portmap", NULL },
	.revision = 0,
	.family = NFPROTO_UNSPEC,
	.dimension = IPSET_DIM_ONE,
	.elem = {
		[IPSET_DIM_ONE - 1] = {
			.parse = ipset_parse_tcp_port,
			.print = ipset_print_port,
			.opt = IPSET_OPT_PORT
		},
	},
	.args = {
		[IPSET_CREATE] = bitmap_port_create_args0,
		[IPSET_ADD] = bitmap_port_add_args0,
	},
	.mandatory = {
		[IPSET_CREATE] = IPSET_FLAG(IPSET_OPT_PORT)
			| IPSET_FLAG(IPSET_OPT_PORT_TO),
		[IPSET_ADD] = IPSET_FLAG(IPSET_OPT_PORT),
		[IPSET_DEL] = IPSET_FLAG(IPSET_OPT_PORT),
		[IPSET_TEST] = IPSET_FLAG(IPSET_OPT_PORT),
	},
	.full = {
		[IPSET_CREATE] = IPSET_FLAG(IPSET_OPT_PORT)
			| IPSET_FLAG(IPSET_OPT_PORT_TO)
			| IPSET_FLAG(IPSET_OPT_TIMEOUT),
		[IPSET_ADD] = IPSET_FLAG(IPSET_OPT_PORT)
			| IPSET_FLAG(IPSET_OPT_PORT_TO)
			| IPSET_FLAG(IPSET_OPT_TIMEOUT),
		[IPSET_DEL] = IPSET_FLAG(IPSET_OPT_PORT)
			| IPSET_FLAG(IPSET_OPT_PORT_TO),
		[IPSET_TEST] = IPSET_FLAG(IPSET_OPT_PORT),
	},

	.usage = bitmap_port_usage0,
	.description = "Initial revision",
};

/* Parse commandline arguments */
static const struct ipset_arg bitmap_port_create_args1[] = {
	{ .name = { "range", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_PORT,
	  .parse = ipset_parse_tcp_port,	.print = ipset_print_port,
	},
	{ .name = { "timeout", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_TIMEOUT,
	  .parse = ipset_parse_timeout,		.print = ipset_print_number,
	},
	{ .name = { "counters", NULL },
	  .has_arg = IPSET_NO_ARG,		.opt = IPSET_OPT_COUNTERS,
	  .parse = ipset_parse_flag,		.print = ipset_print_flag,
	},
	/* Backward compatibility */
	{ .name = { "from", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_PORT,
	  .parse = ipset_parse_single_tcp_port,
	},
	{ .name = { "to", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_PORT_TO,
	  .parse = ipset_parse_single_tcp_port,
	},
	{ },
};

static const struct ipset_arg bitmap_port_add_args1[] = {
	{ .name = { "timeout", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_TIMEOUT,
	  .parse = ipset_parse_timeout,		.print = ipset_print_number,
	},
	{ .name = { "packets", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_PACKETS,
	  .parse = ipset_parse_uint64,		.print = ipset_print_number,
	},
	{ .name = { "bytes", NULL },
	  .has_arg = IPSET_MANDATORY_ARG,	.opt = IPSET_OPT_BYTES,
	  .parse = ipset_parse_uint64,		.print = ipset_print_number,
	},
	{ },
};

static const char bitmap_port_usage1[] =
"create SETNAME bitmap:port range FROM-TO\n"
"               [timeout VALUE] [counters]\n"
"add    SETNAME PORT|FROM-TO [timeout VALUE]\n"
"               [packets VALUE] [bytes VALUE]\n"
"del    SETNAME PORT|FROM-TO\n"
"test   SETNAME PORT\n\n"
"where PORT, FROM and TO are port numbers or port names from /etc/services.\n";

static struct ipset_type ipset_bitmap_port1 = {
	.name = "bitmap:port",
	.alias = { "portmap", NULL },
	.revision = 1,
	.family = NFPROTO_UNSPEC,
	.dimension = IPSET_DIM_ONE,
	.elem = {
		[IPSET_DIM_ONE - 1] = {
			.parse = ipset_parse_tcp_port,
			.print = ipset_print_port,
			.opt = IPSET_OPT_PORT
		},
	},
	.args = {
		[IPSET_CREATE] = bitmap_port_create_args1,
		[IPSET_ADD] = bitmap_port_add_args1,
	},
	.mandatory = {
		[IPSET_CREATE] = IPSET_FLAG(IPSET_OPT_PORT)
			| IPSET_FLAG(IPSET_OPT_PORT_TO),
		[IPSET_ADD] = IPSET_FLAG(IPSET_OPT_PORT),
		[IPSET_DEL] = IPSET_FLAG(IPSET_OPT_PORT),
		[IPSET_TEST] = IPSET_FLAG(IPSET_OPT_PORT),
	},
	.full = {
		[IPSET_CREATE] = IPSET_FLAG(IPSET_OPT_PORT)
			| IPSET_FLAG(IPSET_OPT_PORT_TO)
			| IPSET_FLAG(IPSET_OPT_TIMEOUT)
			| IPSET_FLAG(IPSET_OPT_COUNTERS),
		[IPSET_ADD] = IPSET_FLAG(IPSET_OPT_PORT)
			| IPSET_FLAG(IPSET_OPT_PORT_TO)
			| IPSET_FLAG(IPSET_OPT_TIMEOUT)
			| IPSET_FLAG(IPSET_OPT_PACKETS)
			| IPSET_FLAG(IPSET_OPT_BYTES),
		[IPSET_DEL] = IPSET_FLAG(IPSET_OPT_PORT)
			| IPSET_FLAG(IPSET_OPT_PORT_TO),
		[IPSET_TEST] = IPSET_FLAG(IPSET_OPT_PORT),
	},

	.usage = bitmap_port_usage1,
	.description = "counters support",
};

void _init(void);
void _init(void)
{
	ipset_type_add(&ipset_bitmap_port0);
	ipset_type_add(&ipset_bitmap_port1);
}
