//Hazel Court

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <limits.h>

int primesBelow(int n);
int getPrime(int n, int lo, int hi);
int isPrime(int n);
int main (int argc, char **argv){
    int n = atoi(argv[1]);
    printf("%i", getPrime(n, 1, INT_MAX - 1));
}
int primesBelow(int n){
    int i;
    int primes=0;
    for (i = 1; i < n; i++){
        if (isPrime(i) == 1)
            ++primes;
    }
    return primes;
}

int getPrime(int n, int lo, int hi){
    //This block contains the most naive way to find the nth prime.
    /*
    for (int i = 0; primenum < n; i ++){
        if (isPrime(i) == 1)
            primenum++;
    }*/
    printf("%i + %i\n", lo, hi);
    lo = (unsigned long) lo;
    hi = (unsigned long) hi;
    unsigned long primeguess = (lo+hi)/2;
    unsigned long primeguessnum = primesBelow(primeguess);
    printf("%i, %i\n", primeguess, primeguessnum);
    if (primeguessnum == n){
        while (isPrime(primeguess) == 0){
            primeguess -= 1;
        }
        return primeguess;
    }
    else if (primeguessnum > n){
        return getPrime(n, primeguess, hi);
    }
    else return getPrime(n, lo, primeguess);
     
}

int isPrime(int n){
    int i;
    if (n < 2)
        return 0;
    if (n == 2 || n == 3)
        return 1;
    for (i = 2; i<sqrt(n) + 1; i++){
        if (n % i == 0)
            return 0;
    return 1;
    }
}