using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace stupidbird
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        int gravity = 20;
        int speed = 25;
        int score = 0;


        private void Form1_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Space) 
                gravity = 20;

        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Space)
                gravity = -20;
            else if (e.KeyCode == Keys.Enter)
                score = 0;
                timer1.Start();
        }

        Random rnd = new Random();

        private void timer1_Tick(object sender, EventArgs e)
        {
            bird.Top += gravity;
            pipeDown.Left -= speed;
            pipeTop.Left -= speed;
            lblScore.Text = $"Score: {score}";
            int b = 10;

            if (pipeDown.Left < -170)
            {
                pipeDown.Left = rnd.Next(300, 600);
                score++;
            }
            if(pipeTop.Left < -170)
            {
                int top = rnd.Next(500, 700);
                pipeTop.Left = top;
                score++;
            }
            if(bird.Bounds.IntersectsWith(pipeDown.Bounds)||bird.Bounds.IntersectsWith(pipeTop.Bounds)||bird.Bounds.IntersectsWith(ground.Bounds))
            {
                timer1.Stop();
                lblScore.Text += " Game over !!!";
                

            }
            if (score > b)
                speed += 1;
                b += 10;

            
        }

        

    }
}
