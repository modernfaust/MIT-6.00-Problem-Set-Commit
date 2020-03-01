//Problem Set 2
//An exercise in finding solutions to contrained polynomial equations via exhaustive search

#include <iostream>
#include <vector>
#include <algorithm> 

using namespace std;

int x = 6;
unsigned int mc_nuggets = 0;
vector <int> list1;
vector <int> n;
vector <int> last_6;
bool no_factor = false;
int loop_ctr = 0;
int n_counter = 0;
int a, b, c = 0;
int number = 50;

void clean_up()
{
	sort(list1.begin(), list1.end());
	list1.erase(unique(list1.begin(), list1.end()), list1.end()); //remove duplicates
	list1.erase(remove_if(list1.begin(), list1.end(), [](int n) { return n >= 50; }),
		list1.end()); //remove all values above 50 using C++ lambda
}
void print_it(vector <int> to_print)
{
	int x = 0;
	for (auto value : to_print)
	{
		cout << value << "\n";
	}
}

bool solve_v2(int first, int second, int third, int to_solve)
{
	for (int a = 0; a <= number/first; a++)
	{
		if ((first * a) + (second * b) + (third * c) == to_solve)
		{
			cout << "This value is solvable: " << to_solve << endl;
			return true;
		}
		for (int b = 0; b <= number/second; b++)
		{
			if ((first * a) + (second * b) + (third * c) == to_solve)
			{
				cout << "This value is solvable: " << to_solve << endl;
				return true;
			}
			for (int c = 0; c <= number/third; c++)
			{
				if ((first * a) + (second * b) + (third * c) == to_solve)
				{
					cout << "This value is solvable: " << to_solve << endl;
					return true;
				}
			}
		}
	}
	cout << "This value is unsolvable: " << to_solve << endl;
	return false;
}
int main()
{
	cout << "Please enter the number n that you would like to solve: " << endl;
	cin >> number;
	cout << "Please enter the first value of the diophantine equation: " << endl;
	cin >> a;
	cout << "Please enter the second value of the diophantine equation: " << endl;
	cin >> b;
	cout << "Please enter the third value of the diophantine equation: " << endl;
	cin >> c;
 	for (int i = 0; i <= number; i++)
	{
		if (solve_v2(a,b,c,i) == true)
		{
			list1.push_back(i);
		}
		else
		{
			n.push_back(i);
		}
	}
	if (n.size() !=0)
	{
		cout << "The highest value unsolvable by this equation is: " << n.back() << endl;
	}
	else
	{ }
	return 0;
}
