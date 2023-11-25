#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Date {
  int day;
  int month;
  int year;
};

struct transaction {
  struct Date date;
  char *location[100];
  int fundsout;
  int fundsin;
  };


struct transaction Transactions[100];

void welcomeMenu()
{
  
  printf("Welcome to the simpliiBudget Application\n");
	printf("Inputting your transactions from SIMPLII.csv\n");

  printf("What would you like to do today?\n");
}


void parseCSV(FILE *fptr, struct transaction Transactions)
{ 
  //read in text from csv (comma seperated)
  //
}

int main(){
  
	FILE *fptr;

	if((fptr = fopen("SIMPLII.csv", "r")) == NULL){
			printf("Could not open SIMPLII.csv");
			exit(0);
	}

  welcomeMenu();
  	

	return 0;
}
