# ltspice-analytics-report
Repository for analytics reports generation for LTspice simulation files.




## Spice Commands Breakdown
In this section, typical spice line breakdown is given.

### Resistor
Typical resistor spice line is:

    R5 N003 N005 22k
    
Respectively meanings are:
1. Name
2. Node1
3. Node2 
4. Value 

   
### Capacitor
Typical capacitor spice line is:
    
    C1 N003 N005 10n

Respectively meanings are:
1. Name
2. Node1
3. Node2 
4. Value
    

### Transistor
Typical transistor spice line is:
    
    Q1 N025 P001 0 0 BC847B

Respectively meanings are:
1. Name
2. Collector node
3. Base node
4. Emitter node
5. Substrate (if unspecified, ground used)
6. Model

