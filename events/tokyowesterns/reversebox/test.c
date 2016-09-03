#include <stdio.h>

#define LOBYTE(X) X
#define __ROR1__(X,Y) (X>>Y)|((X<<(8-Y)))
int sub(char *a1, char v18)
{
  unsigned int v1; // eax@1
  int v2; // edx@4
  char v3; // al@5
  char v4; // ST1B_1@7
  char v5; // al@8
  int v6; // eax@10
  int v7; // ecx@10
  int v8; // eax@10
  int v9; // ecx@10
  int v10; // eax@10
  int v11; // ecx@10
  int v12; // eax@10
  int v13; // ecx@10
  int result; // eax@10
  unsigned char v15; // [esp+1Ah] [ebp-Eh]@3
  unsigned char v16; // [esp+1Bh] [ebp-Dh]@3
  char v17; // [esp+1Bh] [ebp-Dh]@7

  *a1 = v18;
  v15 = 1;
  v16 = 1;
  do
  {
    v2 = v15 ^ 2 * v15;
    if ( (v15 & 0x80u) == 0 )
      v3 = 0;
    else
      v3 = 27;
    v15 = v2 ^ v3;
    v4 = 4 * (2 * v16 ^ v16) ^ 2 * v16 ^ v16;
    v17 = 16 * v4 ^ v4;
    if ( v17 >= 0 )
      v5 = 0;
    else
      v5 = 9;
    v16 = v17 ^ v5;
    v6 = (unsigned char)*a1;
    LOBYTE(v6) = v16 ^ v6;
    v7 = v16;
    LOBYTE(v7) = __ROR1__(v16, 7);
    v8 = v7 ^ v6;
    v9 = v16;
    LOBYTE(v9) = __ROR1__(v16, 6);
    v10 = v9 ^ v8;
    v11 = v16;
    LOBYTE(v11) = __ROR1__(v16, 5);
    v12 = v11 ^ v10;
    v13 = v16;
    LOBYTE(v13) = __ROR1__(v16, 4);
    result = v13 ^ v12;
    a1[v15] = result;
  }
  while ( v15 != 1 );
  return result;
}

void main(){
	int i,j;
	unsigned char a[255];
	for(i=0;i<256;i++){
		sub(a,i);
		if(a[84]==0x95){
			for(j=0;j<256;j++){
				printf("\\x%02x",a[j]);
			}
		}
	}
}
