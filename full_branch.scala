import scala.io._
import scala.collection.immutable._

object Bpredict{
  def update_two_bit_counter(table: Array[Int], index: Int, increment: Int) = {
    val counter_value = table(index)
    if (increment == 1)
      if (counter_value != 3)
        table(index) = table(index) + 1
    else
      if (counter_value != 0)
        table(index) = table(index) - 1
  }

  def update_history_register(register: List[Int], branch_outcome: Int) =
    register.tail ::: List(branch_outcome)

  def convert_to_binary(register: Array[Int]) =
    register.foldLeft(0)(_ * 2 + _)

  class Singlebit_Bimodal_Predictor(num_entries: Int){
    val bimod_table: Array[Int] = new Array[Int](num_entries)
      
    def get_prediction(pc: Int) = {
      val index = (pc >> 2) % this.num_entries
      this.bimod_table(index)
    }

    def update(pc: Int, branch_outcome: Int) = {
      val index = (pc >> 2) % this.num_entries
      this.bimod_table(index) = branch_outcome
    }
  }


  class Global_Predictor(num_entries: Int,  bits: Int){  
    var history_register: Array[Int] = new Array[Int](bits)  
    var two_bit_counter_table: Array[Int] = new Array[Int](num_entries)

    def get_prediction(pc: Int) = {
      val index = ((pc >> 2) % this.num_entries) ^ convert_to_binary(this.history_register)
       if (this.two_bit_counter_table(index) > 1) 1 else 0
    }

    def update(pc: Int, branch_outcome: Int) = {
      val index = ((pc >> 2) % this.num_entries) ^ convert_to_binary(this.history_register)
      update_two_bit_counter(this.two_bit_counter_table,index,branch_outcome)
      this.history_register = update_history_register(this.history_register.toList, branch_outcome).toArray
    }
  }


  class Local_Predictor(history_table_size: Int, num_entries: Int, bits: Int){
      val two_bit_counter_table: Array[Int] = new Array[Int](num_entries)
      val history_table: Array[Array[Int]] = new Array(bits * history_table_size)

        for (i <- 1 to num_entries) two_bit_counter_table(i) = 1
        for (i <- 1 to history_table_size){
          for (j <- 1 to bits)
            history_table(i)(j) = 0
        }    

      def get_prediction(pc: Int) = {
        val history_index = (pc >> 2) % this.history_table_size
        val history_register = this.history_table(history_index)
        if (this.two_bit_counter_table(convert_to_binary(history_register)) > 1) 1 else 0
      }

      def update(pc: Int, branch_outcome: Int) = {
        val history_index = (pc >> 2) % this.history_table_size
        val history_register = this.history_table(history_index)
        val index = convert_to_binary(history_register)
        update_two_bit_counter(this.two_bit_counter_table, index, branch_outcome)
        this.history_table(history_index) = update_history_register(history_register.toList, branch_outcome).toArray
      }
    }
    

  class Tournament_Predictor(meta_table_size: Int, local_predictor: Local_Predictor, global_predictor: Global_Predictor){
      val meta_table: Array[Int] = new Array[Int](meta_table_size)  
      var l_prediction = 0
      var g_prediction = 0

      def get_prediction(pc: Int) = {
        val index = convert_to_binary(this.global_predictor.history_register) % this.meta_table_size
        this.g_prediction = this.global_predictor.get_prediction(pc)
        this.l_prediction = this.local_predictor.get_prediction(pc)
        
        if (this.meta_table(index) > 1) this.g_prediction else this.l_prediction
      }

      def update(pc: Int, branch_outcome: Int) = {
        val index = convert_to_binary(this.global_predictor.history_register) % this.meta_table_size
        this.global_predictor.update(pc, branch_outcome)
        this.local_predictor.update(pc, branch_outcome)

        if (this.l_prediction != this.g_prediction)
          if (this.l_prediction == branch_outcome)
            update_two_bit_counter(this.meta_table, index, 0)
          else
            update_two_bit_counter(this.meta_table, index, 1)
      }
  }
    

  class BranchInfo(takenC: Boolean, nTakenC: Boolean, mispred: Boolean)
}

