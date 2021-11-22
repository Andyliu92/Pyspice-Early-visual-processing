#include <iostream>
#include <fstream>

using namespace std;

int main()
{
    ofstream fout("circuit_try.txt");

    long column = 30;
    long row = 30;

    fout << "row = " << row << endl;
    fout << "column = " << column << endl;

    char *r_net = "1.0@u_kOhm";
    fout << "r_net = " << r_net << endl;

    char *r_out = "5@u_kOhm";
    fout << "r_out = " << r_out << endl;

    char *v_ambient = "0@u_V";
    fout << "v_ambient = " << v_ambient << endl;

    char *c = "400@u_uF";
    fout << "c = " << c << endl;

    char *c_init = "0@u_V";
    fout << "c_init = " << c_init << endl;

    fout << "# W-E resistors" << endl;
    for (int i = 1; i <= row; i++)
    {
        for (int j = 1; j < column; j++)
        {
            fout << "circuit.R('" << i << "_" << j << "_" << i << "_" << j + 1 << "', 'net_" << i << "_" << j << "', 'net_" << i << "_" << j + 1 << "', r_net )" << endl;
        }
    }

    fout << endl;
    fout << "# N-S resistors" << endl;
    for (int i = 1; i < row; i++)
    {
        for (int j = 1; j <= column; j++)
        {
            fout << "circuit.R('" << i << "_" << j << "_" << i + 1 << "_" << j << "', 'net_" << i << "_" << j << "', 'net_" << i + 1 << "_" << j << "', r_net)" << endl;
        }
    }

    fout << endl;
    fout << "# NW-SE resistors" << endl;
    for (int i = 1; i < row; i++)
    {
        for (int j = 1; j < column; j++)
        {
            fout << "circuit.R('" << i << "_" << j << "_" << i + 1 << "_" << j + 1 << "', 'net_" << i << "_" << j << "', 'net_" << i + 1 << "_" << j + 1 << "',  r_net )" << endl;
        }
    }

    fout << endl;
    fout << "# NE-SW resistors" << endl;
    for (int i = 1; i < row; i++)
    {
        for (int j = 2; j <= column; j++)
        {
            fout << "circuit.R('" << i << "_" << j << "_" << i + 1 << "_" << j - 1 << "', 'net_" << i << "_" << j << "', 'net_" << i + 1 << "_" << j - 1 << "',  r_net )" << endl;
        }
    }

    fout << endl;
    fout << "# Capacitors" << endl;
    for (int i = 1; i <= row; i++)
    {
        for (int j = 1; j <= column; j++)
        {
            fout << "circuit.C('" << i << "_" << j << "', 'net_" << i << "_" << j << "', circuit.gnd, c )" << endl;
        }
    }

    fout << endl;
    fout << "# Capacitors' Initial Condition" << endl;
    for (int i = 1; i <= row; i++)
    {
        for (int j = 1; j <= column; j++)
        {
            fout << "simulator.initial_condition(net_" << i << "_" << j << "= c_init )" << endl;
        }
    }

    fout << endl;
    fout << "# Output Resistor" << endl;
    for (int i = 1; i <= row; i++)
    {
        for (int j = 1; j <= column; j++)
        {
            fout << "circuit.R('" << i << "_" << j << "', 'net_" << i << "_" << j << "', 'vin_" << i << "_" << j << "', r_out )" << endl;
        }
    }

    fout << endl;
    fout << "# Sensory Inputs" << endl;
    for (int i = 1; i <= row; i++)
    {
        for (int j = 1; j <= column; j++)
        {
            if (j % 2 == 0)
            {
                if (j < column / 2)
                {
                    if (i <= 20 && i >= 10)
                    {
                        fout << "circuit.V('" << i << "_" << j << "', 'vin_" << i << "_" << j << "', 'different_in2',  v_ambient )" << endl;
                        continue;
                    }
                }
                fout << "circuit.V('" << i << "_" << j << "', 'vin_" << i << "_" << j << "', 'different_in1',  v_ambient )" << endl;
                continue;
            }
            if (j > column / 2)
            {
                if (i <= 20 && i >= 10)
                {
                    fout << "circuit.V('" << i << "_" << j << "', 'vin_" << i << "_" << j << "', 'different_in2',  v_ambient )" << endl;
                    continue;
                }
            }
            fout << "circuit.V('" << i << "_" << j << "', 'vin_" << i << "_" << j << "', circuit.gnd,  v_ambient )" << endl;
        }
    }

    fout.close();
}