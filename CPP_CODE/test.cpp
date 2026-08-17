// TODO beolvasni az adatokat

// TODO benyomni őket a >> paramsMLX90641 << ba 

// TODO alkalmazni a kallibrciós function-öket

// TODO beolvasni az adatokat


int HammingDecode(uint16_t *eeData);  
int MLX90641_SynchFrame(uint8_t slaveAddr);







int HammingDecode(uint16_t *eeData)
{
    int error = 0;
    int16_t parity[5];
    int8_t D[16];
    int16_t check;
    uint16_t data;
    uint16_t mask;
    
    for (int addr=16; addr<832; addr++)
    {   
        parity[0] = -1;
        parity[1] = -1;
        parity[2] = -1;
        parity[3] = -1;
        parity[4] = -1;
        
        data = eeData[addr];
        
        mask = 1;
        for( int i = 0; i < 16; i++)
        {          
          D[i] = (data & mask) >> i;
          mask = mask << 1;
        }
        
        parity[0] = D[0]^D[1]^D[3]^D[4]^D[6]^D[8]^D[10]^D[11];
        parity[1] = D[0]^D[2]^D[3]^D[5]^D[6]^D[9]^D[10]^D[12];
        parity[2] = D[1]^D[2]^D[3]^D[7]^D[8]^D[9]^D[10]^D[13];
        parity[3] = D[4]^D[5]^D[6]^D[7]^D[8]^D[9]^D[10]^D[14];
        parity[4] = D[0]^D[1]^D[2]^D[3]^D[4]^D[5]^D[6]^D[7]^D[8]^D[9]^D[10]^D[11]^D[12]^D[13]^D[14]^D[15];
        
        
        if ((parity[0]!=0) || (parity[1]!=0) || (parity[2]!=0) || (parity[3]!=0) || (parity[4]!=0))
        {        
            check = (parity[0]<<0) + (parity[1]<<1) + (parity[2]<<2) + (parity[3]<<3) + (parity[4]<<4);
    
            if ((check > 15)&&(check < 32))
            {
                switch (check)
                {    
                    case 16:
                        D[15] = 1 - D[15];
                        break;
                    
                    case 24:
                        D[14] = 1 - D[14];
                        break;
                        
                    case 20:
                        D[13] = 1 - D[13];
                        break;
                        
                    case 18:
                        D[12] = 1 - D[12];
                        break;                                
                        
                    case 17:
                        D[11] = 1 - D[11];
                        break;
                        
                    case 31:
                        D[10] = 1 - D[10];
                        break;
                        
                    case 30:
                        D[9] = 1 - D[9];
                        break;
                    
                    case 29:
                        D[8] = 1 - D[8];
                        break;                
                    
                    case 28:
                        D[7] = 1 - D[7];
                        break;
                        
                    case 27:
                        D[6] = 1 - D[6];
                        break;
                            
                    case 26:
                        D[5] = 1 - D[5];
                        break;    
                        
                    case 25:
                        D[4] = 1 - D[4];
                        break;     
                        
                    case 23:
                        D[3] = 1 - D[3];
                        break; 
                        
                    case 22:
                        D[2] = 1 - D[2];
                        break; 
                            
                    case 21:
                        D[1] = 1 - D[1];
                        break; 
                        
                    case 19:
                        D[0] = 1 - D[0];
                        break;     
                                     
                }
               
                if(error == 0)
                {
                    error = -9;
                   
                }
                
                data = 0;
                mask = 1;
                for( int i = 0; i < 16; i++)
                {                    
                    data = data + D[i]*mask;
                    mask = mask << 1;
                }
       
            }
            else
            {
                error = -10;                
            }   
        }
        
        eeData[addr] = data & 0x07FF;
    }
    
    return error;
}

int MLX90641_SynchFrame(uint8_t slaveAddr)
{
    uint16_t dataReady = 0;
    uint16_t statusRegister;
    int error = 1;
    
    error = MLX90641_I2CWrite(slaveAddr, 0x8000, 0x0030);
    if(error == -1)
    {
        return error;
    }
    
    while(dataReady == 0)
    {
        error = MLX90641_I2CRead(slaveAddr, 0x8000, 1, &statusRegister);
        if(error != 0)
        {
            return error;
        }    
        dataReady = statusRegister & 0x0008;
    }      
    
   return 0;   
}


