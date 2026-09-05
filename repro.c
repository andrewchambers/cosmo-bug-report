#include <pthread.h>

static void *worker(void *arg) {
  return arg;
}

int main(void) {
  pthread_t thread;
  void *result;
  int error = pthread_create(&thread, 0, worker, 0);
  if (error) return error;
  return pthread_join(thread, &result);
}
