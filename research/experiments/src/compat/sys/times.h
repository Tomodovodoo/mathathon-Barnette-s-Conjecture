/* Minimal replacement for <sys/times.h>, which MinGW does not provide.
   plantri uses it only to report its CPU time. */
#ifndef BX_COMPAT_SYS_TIMES_H
#define BX_COMPAT_SYS_TIMES_H
#include <time.h>
struct tms { clock_t tms_utime, tms_stime, tms_cutime, tms_cstime; };
static clock_t times(struct tms *t)
{
    t->tms_utime = clock();
    t->tms_stime = t->tms_cutime = t->tms_cstime = 0;
    return t->tms_utime;
}
#ifndef CLK_TCK
#define CLK_TCK CLOCKS_PER_SEC
#endif
#endif
