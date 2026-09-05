#define _COSMO_SOURCE
#include <signal.h>
#include <stdint.h>
#include <ucontext.h>
#include <unistd.h>

#define main repro_main
#include "../repro.c"
#undef main

static void value(const char *name, uint64_t x) {
  char buffer[96];
  unsigned n = 0;
  while (*name) buffer[n++] = *name++;
  buffer[n++] = '=';
  buffer[n++] = '0';
  buffer[n++] = 'x';
  for (int shift = 60; shift >= 0; shift -= 4)
    buffer[n++] = "0123456789abcdef"[(x >> shift) & 15];
  buffer[n++] = '\n';
  (void)write(2, buffer, n);
}

static void handler(int sig, siginfo_t *info, void *context) {
  ucontext_t *uc = context;
  value("signal", sig);
  value("si_code", info->si_code);
  value("si_syscall", info->si_syscall);
#ifdef __x86_64__
  value("rip", uc->uc_mcontext.rip);
  value("rax", uc->uc_mcontext.rax);
  value("rbx", uc->uc_mcontext.rbx);
  value("rdi", uc->uc_mcontext.rdi);
  value("rsi", uc->uc_mcontext.rsi);
  value("rdx", uc->uc_mcontext.rdx);
  value("rbp", uc->uc_mcontext.rbp);
  value("rsp", uc->uc_mcontext.rsp);
#endif
  _exit(111);
}

int main(void) {
  struct sigaction action = {0};
  action.sa_sigaction = handler;
  action.sa_flags = SA_SIGINFO;
  sigemptyset(&action.sa_mask);
  if (sigaction(SIGSYS, &action, 0)) return 112;
  return repro_main();
}
