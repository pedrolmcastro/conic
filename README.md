# Conic

A simple program to classify a conic and gather some information about it given its general equation form **ax<sup>2</sup> + bxy + cy<sup>2</sup> + dx + ey + f** with **a**, **b**, and **c** not all equal to zero.

## Usage

Instantiating a Conic object will do all the calculations required and printing it will display its information table.

<table>
    <thead>
        <tr>
            <th colspan = "2"> Attribute </th>
            <th> Description </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan = "2"> name </td>
            <td> Conic classification </td>
        </tr>
        <tr>
            <td rowspan = "3"> center </td>
            <td> <code> tuple </code> </td>
            <td> Center coordinates in the initial equation </td>
        </tr>
        <tr>
            <td> <code> inf </code> </td>
            <td> Infinite centers </td>
        </tr>
        <tr>
            <td> <code> None </code> </td>
            <td> No center </td>
        </tr>
        <tr>
            <td colspan = "2"> angle </td>
            <td> Angle used in the rotation </td>
        </tr>
        <tr>
            <td rowspan = "3"> equations </td>
            <td> <code> [0] </code> </td>
            <td> Initial equation </td>
        </tr>
        <tr>
            <td> <code> [1] </code> </td>
            <td> Equation after translation </td>
        </tr>
        <tr>
            <td> <code> [2] </code> </td>
            <td> Equation after rotation </td>
        </tr>
    </tbody>
</table>
