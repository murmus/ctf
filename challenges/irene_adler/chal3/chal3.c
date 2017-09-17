#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Game stuff:

struct resource{
	char * name;
	char * description;
	unsigned long long int basePrice;
	int decays;
};

#define RESCOUNT 4

struct resource resources[] = {
	{"flag", "flag will get populated here", 1152921504606846976, 0},
	{"gold", "Rare Planetary Metal, very valuable", 100, 0},
	{"computers", "Advanced Computer Components", 75,0},
	{"soylent", "Foodstuff powering all advanced humans", 3, 1},
	{NULL, NULL, 0, 0}
};

#define SHIPCOUNT 4

struct ship {
	char * name;
	char * desc;
	int speed;
	int owned;
	int space;
	unsigned long long int cost;
	unsigned long long int inventory[RESCOUNT];
};

struct ship origShips[] = {
	{"Freighter", "Your basic, starting freighter", 5, 1, 100, 1000, {0, 1, 0, 0}},
	{"Century Hawk", "Fastest Ship in the Galaxy (Kessel Run, etc)", 20, 0, 100, 50000, {0,0,0,0}},
	{"Slug Ship", "Slow, but so much storage space", 1, 0, 1000, 20000, {0,0,0,0}},
	{"Flag Ship", "The God-King's flag ship", 999, 0, 1, 0x200000000, {1,0,0,0}}
};

struct planet {
	int xcoord;
	int ycoord;
	char * name;
	int invVar[RESCOUNT];
};

#define PLANCOUNT 4

struct planet planets[] = {
	{5, 5, "Earth", {100, 50, 50 , 50}},
	{0, 0, "Alpha Centauri", {100, 90, 20, 70}},
	{10, 10, "Trappist 4", {99, 2, 2, 99}},
	{7, 2, "Keppler 17", {100, 20, 20, 20}}
};

static int game_help (lua_State *L){
	printf("To start playing, initialize a new game:\n");
	printf("\t`g = Game.new()`\n");
	return 0;
}

static const luaL_Reg gamelib [] = {
	{"help", game_help},
	{NULL, NULL}
};

static int gameHelp(lua_State *L){
	printf("How to play..\n");
	printf("`g:info()` => Get Current game info\n");
	printf("`g:planetInfo()` => Get info about current planet\n");
	printf("`g:shipInfo()` => Get info about ships in game\n");
	printf("`g:jump(planetId)` => Jump to a planet\n");
	printf("`g:buy(resourceId, count)` => Buy count of resource at currnet market rate\n");
	printf("`g:sell(resourceId, count)` => Sell count of resource at current market rate\n");
	printf("`g:buyFuel(count)` => Buy count units of fuel\n");
	printf("`g:buyShip(shipId)` => Buy shipId\n");
	return 0;
}

struct gamestate{
	unsigned long long int cash;
	int fuel;
	int shipActive;
	int planet;
	struct ship ships[SHIPCOUNT];
};

static int gameNew(lua_State * L){
	printf("initializing game...\n");

	struct gamestate * gs = lua_newuserdata(L, sizeof(struct gamestate));

	luaL_getmetatable(L, "Game");
	lua_setmetatable(L, -2);

	// Populate flag
	FILE * file;

	//CHANGE THIS:
	file = fopen("/home/chal3/flag.txt", "r");
	char * newFlag = malloc(0x100);
	memset(newFlag, 0, 0x100);
	fread(newFlag, 1, 0x100, file);
	fclose(file);

	resources[0].description = newFlag;

	//initialize ships
	memcpy(&gs->ships, origShips, sizeof(origShips));

	gs->cash = 20000;
	gs->fuel = 0x10;
	
	return 1;
}

static struct gamestate * checkState(struct lua_State *L){
	void *ud = luaL_checkudata(L, 1, "Game");
	luaL_argcheck(L, ud!=NULL, 1, "GameState Expected");
	return (struct gamestate *) ud;
}

int gamePInfo(struct lua_State * L){
	struct gamestate * gs = checkState(L);

	printf("Current Planet Stats:\n");
	printf("Name: %s\n\n", planets[gs->planet].name);

	printf("Market:\n");
	int i;
	for(i=0; i<RESCOUNT;i++){
		printf("[%d]\t%s\t@%lld/unit\n", i, resources[i].name, (planets[gs->planet].invVar[i]*resources[i].basePrice)/100);
	}
	printf("\n");

	printf("Jumps:\n");

	for(i=0; i<PLANCOUNT; i++){
		if(i == gs->planet){
			printf("[%d]\t%s\tCURRENT LOCATION\n", i, planets[i].name);
		} else {
			int xdist, ydist;
			xdist = planets[i].xcoord - planets[gs->planet].xcoord;
			if(xdist<0) xdist = ~(xdist)+1;
			ydist = planets[i].ycoord - planets[gs->planet].ycoord;
			if(ydist<0) ydist = ~(ydist)+1;

			printf("[%d]\t%s\t%d Parsecs Away\n", i, planets[i].name, xdist+ydist);
		}

	}

	return 0;
}

int gameInfo(struct lua_State * L){
	struct gamestate * gs = checkState(L);
	printf("Ship: %s\n", gs->ships[gs->shipActive].name);
	printf("Money: %lld\n", gs->cash);
	printf("Fuel: %d\n", gs->fuel);
	printf("Currently on: %s\n", planets[gs->planet].name);

	printf("Inventory:\n");
	int i;
	for(i=0; i < RESCOUNT; i++){
		if(gs->ships[gs->shipActive].inventory[i]){
			printf("\t[%d] %s: %lld\n", i, resources[i].name, gs->ships[gs->shipActive].inventory[i]);
			printf("\t->%s\n", resources[i].description);
		}
	}
	return 0;
}
int gameShipInfo(lua_State * L){
	struct gamestate * gs = checkState(L);

	printf("Ships available are:\n");
	int i;

	for(i=0; i< SHIPCOUNT; i++){
		if(gs->ships[i].owned){
			printf("[%d]\t%s\tOWNED\n", i, gs->ships[i].name);
		} else {
			printf("[%d]\t%s\tNOT OWNED\tAvailabe for %lld\n", i, gs->ships[i].name, gs->ships[i].cost);
		}
		printf("\t->%s\n", gs->ships[i].desc);
	}

	return 0;
}

int gameJump(lua_State * L){
	struct gamestate * gs = checkState(L);
	int pId = luaL_checkinteger(L, 2);

	printf("Jumping to %d\n", pId);
	luaL_argcheck(L, 0<=pId && pId<PLANCOUNT, 2, "PlanetID out of Range");

	if(gs->cash >= 0xffffffff){
		printf("After stalking you for many days, space pirates have finally tracked you down.\n");
		printf("It turns out, carrying around large sums of cash makes you a primary target for pirates\n");
		printf("After a brief struggle, the pirates board and take control of your craft\n");
		printf("While your crew manages to get out of this scrape ok, as captain you aren't so lucky\n");
		printf("At least you got a good view of your ship jumping away in the last seconds before your body froze solid\n");
		exit(0);
	}

	int jumplen;

	int xdist, ydist;
	xdist = planets[pId].xcoord - planets[gs->planet].xcoord;
	if(xdist<0) xdist = ~(xdist)+1;
	ydist = planets[pId].ycoord - planets[gs->planet].ycoord;
	if(ydist<0) ydist = ~(ydist)+1;

	jumplen = xdist + ydist;

	printf("Attempting a jump of %d parsecs to %s\n", jumplen, planets[pId].name);
	int tripTime = jumplen/gs->ships[gs->shipActive].speed;
	printf("Your trip will take %d weeks to make...\n", tripTime);

	int decay = jumplen*7;
	if(decay>100)
		decay = 100;

	if(gs->fuel < jumplen){
		printf("You ran out of fuel on the way...\n");
		if(gs->cash > jumplen*20){
			printf("Luckily, you have enough spare cash to pay the exorbenant price the haulers charge for spare fuel\n");
			printf("It puts you out %d cash, but you make the trip in one piece, although a little slower\n", jumplen*20);
			decay += 10;
			gs->fuel += jumplen;
		} else {
			printf("When the haulers finally show up, they riffle through your cargo.\n");
			printf("Unfortunately for you, they find nothing worth their time, except your bodies\n");
			printf("Like many explorers before you, you spend the rest of your natural life in the collection of a more advanced race\n");
			exit(0);
		}
	}

	gs->fuel -= jumplen;
	int i;
	for(i=0; i<RESCOUNT;i++){
		if(gs->ships[gs->shipActive].inventory[i]){
			if(resources[i].decays){
				printf("During your trip, your %lld units of %s decayed to ", gs->ships[gs->shipActive].inventory[i], resources[i].name);
				gs->ships[gs->shipActive].inventory[i] = ((100-decay)*gs->ships[gs->shipActive].inventory[i])/100;
				printf("%lld units\n", gs->ships[gs->shipActive].inventory[i]);
			}
		}
	}
	gs->planet = pId;
	return 0;
}

int gameBuy(lua_State * L){
	struct gamestate * gs = checkState(L);
	int resId = luaL_checkinteger(L, 2);
	int count = luaL_checkinteger(L, 3);

	luaL_argcheck(L, 0<=resId && resId<RESCOUNT, 2, "Resource out of Range");
	luaL_argcheck(L, 0<=count, 3, "Count out of Range");

	printf("Buying %d of %s\n", count, resources[resId].name);
	unsigned long long int tPrice;
	unsigned long long int max = gs->ships[gs->shipActive].space;
	unsigned long long int cur, i;

	cur = 0;
	for(i=0; i<RESCOUNT; i++){
		cur += gs->ships[gs->shipActive].inventory[i];
	}

	if(cur+count>max){
		printf("Trying to buy %d units (plus %lld in storage), max space is %lld", count, cur, max);
		count = max-cur;
		printf(". Purchasing %d instead.\n", count);
	}

	tPrice = count * ((planets[gs->planet].invVar[resId]*resources[resId].basePrice)/100);

	if(tPrice < ((planets[gs->planet].invVar[resId]*resources[resId].basePrice)/100)){
		printf("Failure to buy\n");
		return 0;
	}

	if(tPrice >= gs->cash){
		printf("Too expensive for your blood\n");
		return 0;
	}

	gs->cash -= tPrice;
	gs->ships[gs->shipActive].inventory[resId] += count;

	return 0;
}
int gameSell(lua_State * L){
	struct gamestate * gs = checkState(L);
	int resId = luaL_checkinteger(L, 2);
	unsigned int count = luaL_checkinteger(L, 3);

	luaL_argcheck(L, 0<=resId && resId<RESCOUNT, 2, "Resource out of Range");
	luaL_argcheck(L, 0<=count, 3, "Count out of Range");

	printf("Selling %d of %s\n", count, resources[resId].name);

	if(count <= gs->ships[gs->shipActive].inventory[resId]){
		gs->ships[gs->shipActive].inventory[resId] -= count;
		gs->cash +=count * ((planets[gs->planet].invVar[resId]*resources[resId].basePrice)/100);
		printf("Sold!\n");
		return 0;
	}
	printf("Did not have enough in current ship...\n");
	return 0;
}
int gameBuyFuel(lua_State * L){
	struct gamestate * gs = checkState(L);
	int count = luaL_checkinteger(L, 2);

	luaL_argcheck(L, 0<=count, 2, "Count out of Range");

	if((gs->fuel + count)>0x1000){
		printf("Maximum fuel 4096, lowering buy to %d\n", count - gs->fuel);
		count = 0x1000 - gs->fuel;
	}

	if(count*10 > gs->cash){
		printf("Not enough money for purchase\n");
		return 0;
	}

	printf("Buying %d units of fuel\n", count);

	gs->fuel += count;
	gs->cash -= count*10;
	return 0;
}
int gameBuyShip(lua_State * L){
	struct gamestate * gs = checkState(L);
	int sId= luaL_checkinteger(L, 2);

	luaL_argcheck(L, 0<=sId && sId < SHIPCOUNT, 2, "ShipId out of Range");

	if(gs->ships[sId].owned){
		printf("You already own %s\n", gs->ships[sId].name);
		return 0;
	}

	if(gs->cash >= gs->ships[sId].cost){
		printf("Purchasing %s for %lld\n", gs->ships[sId].name, gs->ships[sId].cost);
		gs->cash -= gs->ships[sId].cost;
		gs->shipActive = sId;
		return 0;
	}
	printf("You can't afford this...\n");
	return 0;
}

int nullSub(lua_State * L){
	printf("NullSub\n");
	return 0;
}
int gcSub(lua_State *L){
	printf("gc\n");
	return 0;
}
int indSub(lua_State *L){
	printf("indexed\n");
	return 0;
}
int newiSub(lua_State *L){
	printf("NInd\n");
	return 0;
}

static const luaL_Reg game_meta[] = {
	{"__gc", gcSub},
	{"__index", indSub},
	{"__newindex", newiSub},
	{ NULL, NULL }
};

static const luaL_Reg game_methods[] = {
	{"new", gameNew},
	{"help", gameHelp},
	{"planetInfo", gamePInfo},
	{"shipInfo", gameShipInfo},
	{"info", gameInfo},
	{"jump", gameJump},
	{"buy", gameBuy},
	{"sell", gameSell},
	{"buyFuel", gameBuyFuel},
	{"buyShip", gameBuyShip},
	{ NULL, NULL }
};

void makeGame(lua_State* L) {
    int lib_id, meta_id;

    lua_createtable(L, 0, 0);
    lib_id = lua_gettop(L);

    luaL_newmetatable(L, "Game");
    meta_id = lua_gettop(L);
    luaL_setfuncs(L, game_meta, 0);

    luaL_newlib(L, game_methods);
    lua_setfield(L, meta_id, "__index");    

    luaL_newlib(L, game_meta);
    lua_setfield(L, meta_id, "__metatable");

    lua_setmetatable(L, lib_id);

    lua_setglobal(L, "Game");
}

void main(){
	char * inbuf = NULL;
	size_t len = 0;
	lua_State *L;
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);


	int ret;
	
	L = luaL_newstate();

	//luaL_openlibs(L);
	lua_register(L, "help", game_help);

	makeGame(L);

	printf("Use `help()` to get basic help\n");

	while(1){
		lua_gc(L, LUA_GCSTOP, 0);
		inbuf = NULL;
		len = 0;
		getdelim(&inbuf, &len, '\n', stdin);

		//Remove newline
		inbuf[len-1] = '0';

		ret = luaL_loadstring(L, inbuf);
		if(ret){
			printf("Failed to compile\n");
			continue;
		}

		ret = lua_pcall(L, 0, LUA_MULTRET, 0);
		if(ret){
			printf("Failed to run\n");
			continue;
		}

		free(inbuf);
		printf("\n");
		lua_gc(L, LUA_GCRESTART, 0);
	}
}
