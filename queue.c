//queue.c

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "queue.h"

struct queue {
    float arrival;
    float processTime;
    struct queue *next;
    float realStart;
};

customer new_customer(float arrival, float processTime){
    customer result = (customer) malloc(sizeof(queue));
    assert(result!=NULL);
    result->arrival = arrival;
    result->processTime = processTime;
    return result;
}

void free_customer(customer c){
    free((void *) c);
}

customer load_queue(char *filename){
    printf("loading queue...\n");
    FILE *qfp = fopen (filename, "r");
    float arr;
    float pro;
    customer first=NULL;
    customer curr=NULL;
    customer prev=NULL;
    if (qfp != NULL){
        while (feof(qfp)==0){
            fscanf(qfp, "%f", &arr);
            fscanf(qfp, "%f", &pro);
            curr = new_customer(arr, pro);
            if(first==NULL)
                first = curr;
            if(prev!=NULL)
                prev->next=curr;
            prev = curr;
        }
    }
    return (first);
}

void process_queue(customer c){
    printf("processing queue...\n");
    customer next;
    customer curr=c;
    assert(c!=NULL);
    float max_wait=0;
    int max_size=0;
    int curr_size=0;
    customer first = c;
    customer last_process_cust = curr;
    float rs;
    do{
        printf("%i\n", curr_size);
        printf("%i\n", max_size);
        next = curr->next;
        while(last_process_cust!=curr){
            rs=last_process_cust->next->realStart;
            if(rs > curr->arrival){
                while(last_process_cust!=curr){
                ++curr_size;
                last_process_cust=last_process_cust->next;
                }
                break;
            }
            last_process_cust=last_process_cust->next;
        }
        if(curr_size>max_size)
            max_size=curr_size;
        if(curr->realStart - curr->arrival > max_wait)
            max_wait=curr->realStart - curr->arrival;
        curr=next;
    }while (next!=NULL);
    
    printf("Max Size: %i\n", max_size);//2
    printf("Max Wait: %f\n", max_wait);
}

customer get_reals(customer c){
    printf("getting real start times...\n");
    float currTime=0;
    customer curr=c;
    customer next;
    assert(c!=NULL);
    do{
        next = curr->next;
        if(currTime < curr->arrival){
            currTime=curr->arrival;
            curr->realStart=currTime;
        }
        else curr->realStart = currTime;
        currTime+=curr->processTime;
        curr=next;
    }while (next!=NULL);
    
    return c;
}

void free_queue(customer c){
    assert (c!=NULL);
    customer next;
    customer curr=c;
    do{
        next=curr->next;
        free_customer(curr);
    }while(next!=NULL);
}